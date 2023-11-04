import yfinance as yf

import calculator
import terms
import math

import ticker


def average(values):
    value_list = [0 if value is None else value for value in values]
    return sum(value_list) / len(value_list)


def execute_fns(functions):
    for function in functions:
        try:
            result = function()
            if result != 0:
                return result
        except KeyError:
            continue
    return 0


def sum_of_keys(fn, keys, year):
    return_value = 0
    for key in keys:
        try:
            result = fn(key, year)
            if not math.isnan(result):
                return_value += result
        except KeyError:
            continue
    return return_value


class YTicker(ticker.Ticker):
    def __init__(self, tt):
        self.ticker = tt
        self._cache = {}
        self._시가총액 = None
        self._국채수익률 = None
        self._use_non_growth_threshold = False
        self._non_growth_threshold = None
        self._this_year = None
        self._default_yield = None
        self._non_growth_inflation_rate = None
        self._non_growth_dividend_yield = None
        self._dividend_yield = None
        self._default_years = None
        self.element = yf.Ticker(tt)

    def set_use_non_growth_threshold(self, use):
        self._use_non_growth_threshold = use

    def set_국채수익률(self, 국채수익률):
        self._국채수익률 = 국채수익률

    @property
    def 국채수익률(self):
        if self._국채수익률 is None:
            return 0.04285
        return self._국채수익률

    def set_non_growth_threshold(self, year):
        self._non_growth_threshold = year

    @property
    def non_growth_threshold(self):
        if self._non_growth_threshold is None:
            return 5
        return self._non_growth_threshold

    def set_this_year(self, year):
        self._this_year = year

    @property
    def this_year(self):
        if self._this_year is None:
            return self.default_years[-1]
        return self._this_year

    def set_default_years(self, years):
        self._default_years = sorted(years)

    @property
    def default_years(self):
        if self._default_years is None:
            return self.default_data_years
        return self._default_years

    @property
    def default_data_years(self):
        cols = self.element.incomestmt.columns
        years = [col.year for col in cols]
        return years

    def set_non_growth_dividend_yield(self, dividend_yield):
        self._non_growth_dividend_yield = dividend_yield

    @property
    def non_growth_dividend_yield(self):
        if self._non_growth_dividend_yield is None:
            return -0.6
        return self._non_growth_dividend_yield

    def set_non_growth_inflation_rate(self, non_growth_inflation_rate):
        self._non_growth_inflation_rate = non_growth_inflation_rate

    @property
    def non_growth_inflation_rate(self):
        if self._non_growth_inflation_rate is None:
            return 1.025
        return self._non_growth_inflation_rate

    def set_default_yield(self, default_yield):
        self._default_yield = default_yield

    @property
    def default_yield(self):
        if self._default_yield is None:
            raise "default yield is not set"
        return self._default_yield

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

    def 원본데이터(self, year):
        return year in self.default_years

    def 매출액(self, year):
        if (self._use_non_growth_threshold and
                year > self.this_year + self.non_growth_threshold):
            value = self.매출액(year - 1) * self.non_growth_inflation_rate
        elif year in self.default_years:
            value = self._손익계산서(terms.TotalRevenue, year)
            if value == 0:
                raise Exception(f"total revenue is not exist in real data in ${year} years")
        else:
            value = self.매출액(year - 1) * (1 + self.평균매출액증가율())
        return value

    def 평균매출액증가율(self):
        if self._cache.get("평균매출액증가율") is not None:
            return self._cache.get("평균매출액증가율")

        total_sales_growth_rate = 0
        len_years = len(self.default_years)
        for i in range(len_years):
            if i != len_years - 1:
                prev_year = self.default_years[i + 1]
                nxt_year = self.default_years[i]
                sales_growth_rate = (
                        (self.매출액(nxt_year) - self.매출액(prev_year)) /
                        self.매출액(prev_year)
                )
                total_sales_growth_rate += sales_growth_rate
        self._cache["평균매출액증가율"] = total_sales_growth_rate / len_years
        return self._cache["평균매출액증가율"]

    def 매출원가(self, year):
        if year in self.default_years:
            value = self._손익계산서(terms.CostOfRevenue, year)
            if value == 0:
                raise Exception(f"cost of revenue is not exist in real data in ${year} years")
        else:
            value = self.매출액(year) * self.평균매출원가율()
        return value

    def 평균매출원가율(self):
        if self._cache.get("평균매출원가율") is not None:
            return self._cache.get("평균매출원가율")
        total_cost_of_revenue = 0
        for year in self.default_years:
            total_cost_of_revenue += (self.매출원가(year) / self.매출액(year))
        self._cache["평균매출원가율"] = total_cost_of_revenue / len(self.default_years)
        return self._cache["평균매출원가율"]

    def 매출총이익(self, year):
        if year in self.default_years:
            value = self._손익계산서(terms.GrossProfit, year)
            if value == 0:
                raise Exception(f"gross profit is not exist in real data in ${year} years")
        else:
            value = self.매출액(year) - self.매출원가(year)
        return value

    def 판매비와관리비(self, year):
        return execute_fns([
            lambda: sum_of_keys(self._손익계산서, [terms.SellingGeneralAndAdministration], year),
            lambda: sum_of_keys(
                self._손익계산서,
                [terms.SellingAndMarketingExpense, terms.GeneralAndAdministrativeExpense],
                year
            ),
            lambda: self.매출액(year) * self.매출액대비판관비율()
        ])

    def 매출액대비판관비율(self):
        if self._cache.get("매출액대비판관비율") is not None:
            return self._cache.get("매출액대비판관비율")
        total_sg_n_a_percent = 0
        for year in self.default_years:
            total_sg_n_a_percent += (self.판매비와관리비(year) / self.매출액(year))
        self._cache["매출액대비판관비율"] = total_sg_n_a_percent / len(self.default_years)
        return self._cache["매출액대비판관비율"]

    def 영업이익(self, year):
        if year in self.default_years:
            value = self._손익계산서(terms.OperatingIncome, year)
            if value == 0:
                raise Exception(f"operating income is not exist in real data in ${year} years")
        else:
            value = self.매출총이익(year) - self.판매비와관리비(year)
        return value

    def 지분법손익(self, year):
        if year in self.default_years:
            return self._손익계산서(terms.NetIncomeIncludingNonControllingInterests, year)
        else:
            return average([self.지분법손익(y) for y in self.default_years])

    def 금융손익(self, year):
        if year in self.default_years:
            return sum_of_keys(self._손익계산서, terms.금융손익리스트, year)
        else:
            return average([self.금융손익(y) for y in self.default_years])

    def 기타손익(self, year):
        if year in self.default_years:
            return sum_of_keys(self._손익계산서, terms.기타손익리스트, year)
        else:
            return average([self.기타손익(y) for y in self.default_years])

    def 법인세비용차감전순이익(self, year):
        if year in self.default_years:
            value = self._손익계산서(terms.PretaxIncome, year)
            if value == 0:
                raise Exception(f"pretax income is not exist in real data in ${year} years")
        else:
            value = self.영업이익(year) + self.지분법손익(year) + self.금융손익(year) + self.기타손익(year)
        return value

    def 법인세비용(self, year):
        return execute_fns([
            lambda: self._손익계산서(terms.TaxProvision, year),
            lambda: self.법인세비용차감전순이익(year) * self.평균유효세율()
        ])

    def 평균유효세율(self):
        if self._cache.get("평균유효세율") is not None:
            return self._cache.get("평균유효세율")
        total_tax_rate = 0
        for year in self.default_years:
            total_tax_rate += self.법인세비용(year) / self.법인세비용차감전순이익(year)
        self._cache["평균유효세율"] = total_tax_rate / len(self.default_years)
        return self._cache["평균유효세율"]

    def 당기순이익(self, year):
        if year in self.default_years:
            value = self._손익계산서(terms.NetIncome, year)
            if value == 0:
                raise Exception(f"net income is not exist in real data in ${year} years")
        else:
            value = self.법인세비용차감전순이익(year) - self.법인세비용(year)
        return value

    def 주주환원식(self, year):
        if year not in self.default_years:
            return 0

        현금배당 = execute_fns([
            lambda: sum_of_keys(self._현금흐름표, [terms.CashDividendsPaid], year),
            lambda: sum_of_keys(self._현금흐름표, [terms.CommonStockDividendPaid], year),
        ])
        자사주매입 = sum_of_keys(self._현금흐름표, [terms.RepurchaseOfCapitalStock], year)
        if 자사주매입 == 0:
            stockpayment = sum_of_keys(self._현금흐름표, [terms.CommonStockPayments], year)
            if stockpayment < 0:
                자사주매입 = stockpayment

        return 현금배당 + 자사주매입

    def 주주환원(self, year):
        if year in self.default_years:
            return self.주주환원식(year)
        return self.주주환원율(year) * self.당기순이익(year)

    def 주주환원율(self, year):
        if (self._use_non_growth_threshold and
                year > self.this_year + self.non_growth_threshold):
            return self.non_growth_dividend_yield
        if year in self.default_years:
            return self.주주환원식(year)/self.당기순이익(year)
        return self.평균주주환원율()

    def 평균주주환원율(self):
        if self._cache.get("평균주주환원율") is not None:
            return self._cache.get("평균주주환원율")

        total_cost = 0
        cnt = 0
        for y in self.default_years:
            주주환원 = self.주주환원식(y)
            if 주주환원 != 0:
                cost = 주주환원 / self.당기순이익(y)
                total_cost += cost
                cnt += 1
        self._cache["평균주주환원율"] = total_cost / cnt
        return self._cache["평균주주환원율"]

    def 예상할인율(self):
        if self._cache.get("예상할인율") is not None:
            return self._cache.get("예상할인율")
        cashflow = [-1 * self.시가총액()] + [-1 * self.주주환원(y) for y in range(2020, 2040)]
        self._cache["예상할인율"] = calculator.irr(cashflow)
        return self._cache["예상할인율"]

    def set_시가총액(self, 시가총액):
        self._시가총액 = 시가총액

    def 시가총액(self):
        if self._시가총액 is not None:
            return self._시가총액
        return self.element.fast_info[terms.MarketCap]

    def 리스크프리미엄(self):
        return self.예상할인율() - self.국채수익률
