from abc import ABC, abstractmethod
import FinanceDataReader as fdr
import datetime
import calculator
import math


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


def execute_fns(functions):
    for function in functions:
        try:
            result = function()
            if result != 0:
                return result
        except KeyError:
            continue
    return 0


def average(values):
    value_list = [0 if value is None else value for value in values]
    return sum(value_list) / len(value_list)


def 국채수익률(tt):
    data = fdr.DataReader(tt)
    latest = data.index[-1]
    return data.loc[latest].iloc[4] / 100


class Ticker(ABC):

    def __init__(self, tt):
        self.ticker = tt
        self._cache = {}
        self._first_year = None
        self._use_non_growth_threshold = None
        self._use_non_growth_threshold = False
        self._non_growth_threshold = None
        self._this_year = None
        self._non_growth_inflation_rate = None
        self._non_growth_dividend_yield = None
        self._dividend_yield = None

    @abstractmethod
    def can_use(self):
        pass

    def set_use_non_growth_threshold(self, use):
        self._use_non_growth_threshold = use

    @abstractmethod
    def 국채수익률(self):
        pass

    def set_non_growth_threshold(self, year):
        self._non_growth_threshold = year

    @property
    def non_growth_threshold(self) -> int:
        if self._non_growth_threshold is None:
            return 5
        return self._non_growth_threshold

    def set_non_growth_inflation_rate(self, non_growth_inflation_rate):
        self._non_growth_inflation_rate = non_growth_inflation_rate

    @property
    def non_growth_inflation_rate(self):
        if self._non_growth_inflation_rate is None:
            return 1.025
        return self._non_growth_inflation_rate

    @abstractmethod
    def first_year(self) -> int:
        pass

    @property
    def this_year(self) -> int:
        return datetime.datetime.today().year

    def set_use_non_growth_threshold(self, use):
        self._use_non_growth_threshold = use

    def set_non_growth_dividend_yield(self, non_growth_dividend_yield):
        self._non_growth_dividend_yield = non_growth_dividend_yield

    @property
    def non_growth_dividend_yield(self):
        return self._non_growth_dividend_yield

    @abstractmethod
    def 손익계산서(self, year):
        pass

    @abstractmethod
    def 재무상태표(self, year):
        pass

    @abstractmethod
    def 현금흐름표(self, year):
        pass

    def 원본데이터(self, year):
        return self.first_year() <= year < self.this_year

    @abstractmethod
    def _매출액(self, year):
        pass

    def 매출액(self, year):
        if (self._use_non_growth_threshold and
                year >= self.this_year + self.non_growth_threshold):
            value = self.매출액(year - 1) * self.non_growth_inflation_rate
        elif year < self.this_year:
            return self._매출액(year)
        else:
            value = self.매출액(year - 1) * (1 + self.평균매출액증가율())
        return value

    def 평균매출액증가율(self):
        if self._cache.get("평균매출액증가율") is not None:
            return self._cache.get("평균매출액증가율")

        total_sales_growth_rate = 0
        for i in range(self.first_year(), self.this_year - 1):
            prev_year = i
            nxt_year = i + 1
            sales_growth_rate = (
                    (self.매출액(nxt_year) - self.매출액(prev_year)) /
                    self.매출액(prev_year)
            )
            total_sales_growth_rate += sales_growth_rate
        self._cache["평균매출액증가율"] = total_sales_growth_rate / (self.this_year - self.first_year())
        return self._cache["평균매출액증가율"]

    @abstractmethod
    def _매출원가(self, year):
        pass

    def 매출원가(self, year):
        if year < self.this_year:
            return self._매출원가(year)
        else:
            value = self.매출액(year) * self.평균매출원가율()
        return value

    def 평균매출원가율(self):
        if self._cache.get("평균매출원가율") is not None:
            return self._cache.get("평균매출원가율")
        total_cost_of_revenue = 0
        for year in range(self.first_year(), self.this_year):
            total_cost_of_revenue += (self.매출원가(year) / self.매출액(year))
        self._cache["평균매출원가율"] = total_cost_of_revenue / (self.this_year - self.first_year())
        return self._cache["평균매출원가율"]

    @abstractmethod
    def _매출총이익(self, year):
        pass

    def 매출총이익(self, year):
        if year < self.this_year:
            return self._매출총이익(year)
        else:
            value = self.매출액(year) - self.매출원가(year)
        return value

    @abstractmethod
    def _판매비와관리비(self, year):
        pass

    def 판매비와관리비(self, year):
        if year < self.this_year:
            return self._판매비와관리비(year)
        else:
            value = self.매출액(year) * self.매출액대비판관비율()
        return value

    def 매출액대비판관비율(self):
        if self._cache.get("매출액대비판관비율") is not None:
            return self._cache.get("매출액대비판관비율")
        total_sg_n_a_percent = 0
        for year in range(self.first_year(), self.this_year):
            total_sg_n_a_percent += (self.판매비와관리비(year) / self.매출액(year))
        self._cache["매출액대비판관비율"] = total_sg_n_a_percent / (self.this_year - self.first_year())
        return self._cache["매출액대비판관비율"]

    @abstractmethod
    def _영업이익(self, year):
        pass

    def 영업이익(self, year):
        if year < self.this_year:
            return self._영업이익(year)
        else:
            value = execute_fns([
                lambda: self.매출총이익(year) - self.판매비와관리비(year),
                lambda: self.매출액(year) * self.영업이익율()
            ])
        return value

    def 영업이익율(self):
        if self._cache.get("영업이익율") is not None:
            return self._cache.get("영업이익율")
        elem = 0
        for year in self.default_years:
            elem += (self.매출액(year) / self.영업이익(year))
        self._cache["영업이익율"] = elem / len(self.default_years)
        return self._cache["영업이익율"]

    @abstractmethod
    def _지분법손익(self, year):
        pass

    def 지분법손익(self, year):
        if year < self.this_year:
            return self._지분법손익(year)
        else:
            return average([self.지분법손익(y) for y in range(self.first_year(), self.this_year)])

    @abstractmethod
    def _금융손익(self, year):
        pass

    def 금융손익(self, year):
        if year < self.this_year:
            return self._금융손익(year)
        else:
            return average([self.금융손익(y) for y in range(self.first_year(), self.this_year)])

    @abstractmethod
    def _기타손익(self, year):
        pass

    def 기타손익(self, year):
        if year < self.this_year:
            return self._기타손익(year)
        else:
            return average([self.기타손익(y) for y in range(self.first_year(), self.this_year)])

    @abstractmethod
    def _법인세비용차감전순이익(self, year):
        pass

    def 법인세비용차감전순이익(self, year):
        if year < self.this_year:
            value = self._법인세비용차감전순이익(year)
        else:
            value = self.영업이익(year) + self.지분법손익(year) + self.금융손익(year) + self.기타손익(year)
        return value

    @abstractmethod
    def _법인세비용(self, year):
        pass

    def 법인세비용(self, year):
        if year < self.this_year:
            value = self._법인세비용(year)
        else:
            value = self.법인세비용차감전순이익(year) * self.평균유효세율()
        return value

    def 평균유효세율(self):
        if self._cache.get("평균유효세율") is not None:
            return self._cache.get("평균유효세율")
        total_tax_rate = 0
        for year in range(self.first_year(), self.this_year):
            total_tax_rate += self.법인세비용(year) / self.법인세비용차감전순이익(year)
        self._cache["평균유효세율"] = total_tax_rate / (self.this_year - self.first_year())
        return self._cache["평균유효세율"]

    @abstractmethod
    def _당기순이익(self, year) -> float:
        pass

    def 당기순이익(self, year):
        if year < self.this_year:
            value = self._당기순이익(year)
        else:
            value = self.법인세비용차감전순이익(year) - self.법인세비용(year)
        return value

    @abstractmethod
    def _주주환원(self, year) -> float:
        pass

    def 주주환원(self, year) -> float:
        if year < self.this_year:
            return self._주주환원(year)
        return self.주주환원율(year) * self.당기순이익(year)

    def 주주환원율(self, year):
        if (self._use_non_growth_threshold and
                year > self.this_year + self.non_growth_threshold):
            return self.non_growth_dividend_yield
        if year < self.this_year:
            return self._주주환원(year) / self.당기순이익(year)
        return self.평균주주환원율()

    def 평균주주환원율(self):
        if self._cache.get("평균주주환원율") is not None:
            return self._cache.get("평균주주환원율")

        total = 0
        cnt = self.this_year - self.first_year()
        for y in range(self.first_year(), self.this_year):
            total += self.주주환원율(y)
        self._cache["평균주주환원율"] = total / cnt
        return self._cache["평균주주환원율"]

    def 예상할인율(self):
        if self._cache.get("예상할인율") is not None:
            return self._cache.get("예상할인율")
        cashflow = [-1 * self.시가총액()]
        cashflow += [-1 * self.주주환원(y) for y in range(2020, 2040)]
        self._cache["예상할인율"] = calculator.irr(cashflow)
        return self._cache["예상할인율"]

    @abstractmethod
    def 시가총액(self) -> float:
        pass

    def 리스크프리미엄(self):
        return self.예상할인율() - self.국채수익률()

    def info(self):
        return {
            "Ticker": self.ticker,
            "시가 총액": self.시가총액(),
            "평균 매출액 증가율": self.평균매출액증가율(),
            "예상 할인율": self.예상할인율(),
            "평균 주주 환원율": -1 * self.평균주주환원율(),
            "리스크 프리미엄": self.리스크프리미엄(),
        }

    def financial_info(self, year):
        try:
            result = {
                "원본 데이터": self.원본데이터(year),
                "매출 액": self.매출액(year),
                "매출 원가": self.매출원가(year),
                "매출 총 이익": self.매출총이익(year),
                "판매비 와 관리바": self.판매비와관리비(year),
                "영업 이익": self.영업이익(year),
                "지분법 손익": self.지분법손익(year),
                "금융 손익": self.금융손익(year),
                "기타 손익": self.기타손익(year),
                "법인세비용 차감전 순이익": self.법인세비용차감전순이익(year),
                "법인세 비용": self.법인세비용(year),
                "당기 순이익": self.당기순이익(year),
                "주주 환원율": -1 * self.주주환원율(year),
                "주주 환원": -1 * self.주주환원(year)
            }
        except KeyError:
            result = {
                "원본 데이터": self.원본데이터(year),
                "매출 액": self.매출액(year),
                "영업 이익": self.영업이익(year),
                "지분법 손익": self.지분법손익(year),
                "금융 손익": self.금융손익(year),
                "기타 손익": self.기타손익(year),
                "법인세비용 차감전 순이익": self.법인세비용차감전순이익(year),
                "법인세 비용": self.법인세비용(year),
                "당기 순이익": self.당기순이익(year),
                "주주 환원율": -1 * self.주주환원율(year),
                "주주 환원": -1 * self.주주환원(year)
            }
        return result


if __name__ == "__main__":
    stocks = fdr.StockListing('KRX')
    stocks = stocks[stocks['Code'] == "323410"]['Marcap'].values[0]
    print(stocks)
    # latest = data.index[-1]
    #  data.loc[latest].iloc[4] / 100
