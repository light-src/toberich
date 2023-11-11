import yfinance as yf

import yterms

import ticker
from ticker import execute_fns, sum_of_keys, 국채수익률


class YTicker(ticker.Ticker):
    def 국채수익률(self):
        return 국채수익률("US10YT")

    def can_use(self):
        return True

    def __init__(self, tt):
        super().__init__(tt)
        self._first_year = 0
        self._default_years = None
        self.element = yf.Ticker(tt)

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

    def _손익계산서(self, index, year):
        day = self.target_day(year)
        return self.element.incomestmt.loc[index][day]

    def _재무상태표(self, index, year):
        day = self.target_day(year)
        return self.element.balancesheet.loc[index][day]

    def _현금흐름표(self, index, year):
        day = self.target_day(year)
        return self.element.cashflow.loc[index][day]

    def 손익계산서(self, year):
        day = self.target_day(year)
        return self.element.incomestmt[day]

    def 재무상태표(self, year):
        day = self.target_day(year)
        return self.element.balancesheet[day]

    def 현금흐름표(self, year):
        day = self.target_day(year)
        return self.element.cashflow[day]

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


if __name__ == "__main__":
    d = YTicker("META").손익계산서(2022)
    print(d.index)
    print(d)
