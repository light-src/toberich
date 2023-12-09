import json

import pandas
import yfinance as yf

import db
import yterms
import ticker
from ticker import execute_fns, sum_of_keys, 국채수익률

SOURCE = "yahoo"


class YTicker(ticker.Ticker):
    def account(self, account):
        accounts = []
        fns = [self._손익계산서, self._현금흐름표, self._재무상태표]
        for fn in fns:
            try:
                accounts = [fn(account, year) for year in self.default_years]
            except Exception:
                continue
        return accounts

    def 국채수익률(self):
        return 국채수익률("US10YT")

    def can_use(self) -> bool:
        try:
            self.손익계산서(2022)
        except Exception:
            return False
        return True

    def __init__(self, tt):
        super().__init__(tt)
        self.db = db.SQLiteDatabase()
        self._first_year = 0
        self._default_years = None
        self.element = yf.Ticker(tt)

    def __del__(self):
        self.db.close_connection()

    def set_default_years(self, years):
        self._default_years = sorted(years)

    @property
    def default_years(self):
        if self._default_years is None:
            return self.default_data_years
        return self._default_years

    @property
    def default_data_years(self):
        if self._cache.get("default_data_years") is not None:
            return self._cache.get("default_data_years")
        cols = self.element.incomestmt.columns
        years = [col.year for col in cols]
        self._cache["default_data_years"] = years
        return self._cache["default_data_years"]

    def first_year(self):
        return self.default_years[len(self.default_data_years) - 1]

    def target_day(self, year):
        days = self.element.incomestmt.columns
        min_year = days[len(days) - 1].year

        if year < min_year:
            raise Exception("min year have to be at most " + str(min_year))

        for day in days:
            if day.year == year:
                return day

        return str(year) + "-12-31"

    def _매출액(self, year):
        value = self._손익계산서(yterms.TotalRevenue, year)
        if value == 0:
            raise Exception(f"total revenue is not exist in real data in ${year} year")
        return value

    def _매출원가(self, year):
        value = self._손익계산서(yterms.CostOfRevenue, year)
        if value == 0:
            raise Exception(f"cost of revenue is not exist in real data in ${year} years")
        return value

    def _매출총이익(self, year):
        value = self._손익계산서(yterms.GrossProfit, year)
        if value == 0:
            raise Exception(f"gross profit is not exist in real data in ${year} years")
        return value

    def _판매비와관리비(self, year):
        return execute_fns([
            lambda: sum_of_keys(self._손익계산서, [yterms.SellingGeneralAndAdministration], year),
            lambda: sum_of_keys(
                self._손익계산서,
                [yterms.SellingAndMarketingExpense, yterms.GeneralAndAdministrativeExpense],
                year
            ),
        ])

    def _영업이익(self, year):
        value = execute_fns([
            lambda: self._손익계산서(yterms.OperatingIncome, year),
            lambda: self._손익계산서(yterms.OperatingRevenue, year) - self._손익계산서(yterms.OperatingExpense, year),
        ])
        if value == 0:
            raise Exception(f"operating income is not exist in real data in ${year} years")
        return value

    def _지분법손익(self, year):
        value = self._손익계산서(yterms.NetIncomeIncludingNonControllingInterests, year)
        if value == 0:
            raise Exception(f"NetIncomeIncludingNonControllingInterests not exist in real data in {year}")

    def _금융손익(self, year):
        return sum_of_keys(self._손익계산서, yterms.금융손익리스트, year)

    def _기타손익(self, year):
        return sum_of_keys(self._손익계산서, yterms.기타손익리스트, year)

    def _법인세비용차감전순이익(self, year):
        value = self._손익계산서(yterms.PretaxIncome, year)
        if value == 0:
            raise Exception(f"pretax income is not exist in real data in ${year} years")
        return value

    def _법인세비용(self, year):
        return self._손익계산서(yterms.TaxProvision, year)

    def _당기순이익(self, year):
        value = self._손익계산서(yterms.NetIncome, year)
        if value == 0:
            raise Exception(f"net income is not exist in real data in ${year} years")
        return value

    def _주주환원(self, year):
        if year not in self.default_years:
            return 0

        현금배당 = execute_fns([
            lambda: sum_of_keys(self._현금흐름표, [yterms.CashDividendsPaid], year),
            lambda: sum_of_keys(self._현금흐름표, [yterms.CommonStockDividendPaid], year),
        ])
        자사주매입 = sum_of_keys(self._현금흐름표, [yterms.RepurchaseOfCapitalStock], year)
        if 자사주매입 == 0:
            stockpayment = sum_of_keys(self._현금흐름표, [yterms.CommonStockPayments], year)
            if stockpayment < 0:
                자사주매입 = stockpayment

        return 현금배당 + 자사주매입

    def 시가총액(self):
        return self.element.fast_info[yterms.MarketCap]

    def _손익계산서(self, index, year):
        return self.손익계산서(year).loc[index]

    def _재무상태표(self, index, year):
        return self.재무상태표(year).loc[index]

    def _현금흐름표(self, index, year):
        return self.현금흐름표(year).loc[index]

    def 손익계산서(self, year):
        return self._재무제표(self.element.get_incomestmt, db.INCOMESTMT, year)

    def 재무상태표(self, year):
        return self._재무제표(self.element.get_balancesheet, db.BALANCESHEET, year)

    def 현금흐름표(self, year):
        return self._재무제표(self.element.get_cashflow, db.CASHFLOW, year)

    def _재무제표(self, fn, type, year):
        key = f"{type}{year}"
        if self._cache.get(key) is not None:
            return self._cache[key]

        value = self.db.select_data(self.ticker, year, SOURCE, type)
        if value is None:
            day = self.target_day(year)
            data = fn(pretty=True)[day]
            self.db.insert_data(self.ticker, year, type, SOURCE, data.to_json())
        else:
            data_dict = json.loads(value[0][0])
            data = pandas.DataFrame(data_dict.values(), index=data_dict.keys())[0]

        self._cache[key] = data
        return self._cache[key]


if __name__ == "__main__":
    pass
    # from slack_finance_response import int_format
    #
    d_b = db.SQLiteDatabase()
    d_b.create_table_if_not_exists()
    d_b.close_connection()
    #
    d = YTicker("035420.ks")
    print(d.info())
    # print(d.financial_info(2022))
    # print(f"평균 유효세율 {int_format(d.평균유효세율())}")
    # for y in range(2020, 2030):
    #     print(f"---------{y}---------")
    #     print(f"법인세 차감전 순이익 {int_format(d.법인세비용차감전순이익(y))}")
    #     print(f"매출액 {int_format(d.매출액(y))} 매출원가 {int_format(d.매출원가(y))} 영업이익 {int_format(d.영업이익(y))} "
    #           f"영업이익률 {int_format(d.영업이익(y) / d.매출액(y) )}")
    #     print(f"주주환원율 {int_format(d.주주환원율(y))}")
    #     print(f"당기순이익 {int_format(d.당기순이익(y))} 주주환원 {int_format(d.주주환원(y))} 영업이익 {int_format(d.영업이익(y))} 지분법손익 {int_format(d.지분법손익(y))} 금융손익 {int_format(d.금융손익(y))} 기타손익 {int_format(d.기타손익(y))} 법인세비용 {int_format(d.법인세비용(y))}")
