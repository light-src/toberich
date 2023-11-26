import json
import os

import db
from ticker import sum_of_keys
import ticker
import OpenDartReader
import dart_terms
import pandas as pd
import FinanceDataReader as fdr

SOURCE = "dart"


def to_float(value) -> float:
    try:
        return float(value)
    except Exception:
        return 0


class DartTicker(ticker.Ticker):
    def 국채수익률(self):
        return 3.960/100

    def 시가총액(self) -> float:
        tt = self.ticker.replace(".ks", "")
        stocks = fdr.StockListing('KRX')
        return stocks[stocks['Code'] == tt]['Marcap'].values[0]

    def __init__(self, tt):
        api_key = os.getenv("DART_API_TOKEN")
        super().__init__(tt)
        self.db = db.SQLiteDatabase()
        self._cache = {}
        self.ticker = tt
        self.dart = OpenDartReader(api_key)

    def __del__(self):
        self.db.close_connection()

    def can_use(self) -> bool:
        if not self.ticker.endswith(".ks"):
            return False
        try:
            self.손익계산서(2022)
        except Exception:
            return False
        return True

    def first_year(self) -> int:
        if self._cache.get("first_year") is not None:
            return self._cache.get("first_year")
        for year in range(2015, self.this_year):
            value = self._매출액(year)
            if value != 0:
                self._cache["first_year"] = year
                return year
        return self.this_year

    def _매출액(self, year):
        return sum_of_keys(self._손익계산서, [dart_terms.매출액, dart_terms.수익매출액], year)

    def _매출원가(self, year):
        return self._손익계산서(dart_terms.매출원가, year)

    def _매출총이익(self, year):
        return self._손익계산서(dart_terms.매출총이익, year)

    def _판매비와관리비(self, year):
        return self._손익계산서(dart_terms.판매비와관리비, year)

    def _영업이익(self, year):
        return self._손익계산서(dart_terms.영업이익, year)

    def _지분법손익(self, year):
        return self._손익계산서(dart_terms.지분법수익, year) - self._손익계산서(dart_terms.지분법비용, year)

    def _금융손익(self, year):
        return self._손익계산서(dart_terms.금융수익, year) - self._손익계산서(dart_terms.금융비용, year)

    def _기타손익(self, year):
        return self._손익계산서(dart_terms.기타수익, year) - self._손익계산서(dart_terms.기타비용, year)

    def _법인세비용차감전순이익(self, year):
        return self._손익계산서(dart_terms.법인세비용차감전순이익, year)

    def _법인세비용(self, year):
        return self._손익계산서(dart_terms.법인세비용, year)

    def _당기순이익(self, year) -> float:
        return self._손익계산서(dart_terms.당기순이익, year)

    def _주주환원(self, year) -> float:
        현금배당 = self._현금흐름표(dart_terms.배당금의지급, year)
        자사주매입 = self._현금흐름표(dart_terms.자기주식의취득, year)

        return -1 * (현금배당 + 자사주매입)

    def _손익계산서(self, index, year):
        try:
         value = self.손익계산서(year).loc[index]
        except KeyError:
            value = 0
        return to_float(value)

    def _재무상태표(self, index, year):
        try:
         value = self.재무상태표(year).loc[index]
        except KeyError:
            value = 0
        return to_float(value)

    def _현금흐름표(self, index, year):
        try:
         value = self.현금흐름표(year).loc[index]
        except KeyError:
            value = 0
        if value == '':
            value = 0
        return to_float(value)

    def 손익계산서(self, year):
        try:
            return self._재무제표("손익계산서", db.INCOMESTMT, year)
        except Exception:
            return self._재무제표("포괄손익계산서", db.INCOMESTMT, year)

    def 재무상태표(self, year):
        return self._재무제표("재무상태표", db.BALANCESHEET, year)

    def 현금흐름표(self, year):
        return self._재무제표("현금흐름표", db.CASHFLOW, year)

    def _재무제표(self, elem, type, year):
        key = str(elem) + str(year)
        if self._cache.get(key) is not None:
            return self._cache.get(key)

        value = self.db.select_data(self.ticker, year, SOURCE, type)
        if value is None:
            tt = self.ticker.replace(".ks", "")
            df = self.dart.finstate_all(tt, year)
            raw = df[df['sj_nm'] == elem]
            keys = raw['account_nm'].tolist()
            values = raw['thstrm_amount'].tolist()
            data = pd.DataFrame(values, index=keys)[0]
            self.db.insert_data(self.ticker, year, type, SOURCE, data.to_json())
        else:
            data_dict = json.loads(value[0][0])
            data = pd.DataFrame(data_dict.values(), index=data_dict.keys())[0]

        self._cache[key] = data
        return self._cache[key]


if __name__ == "__main__":
    pass
    # from slack_finance_response import int_format
    # d = DartTicker("035420")
    # d.info()
    # print(f"평균 유효세율 {int_format(d.평균유효세율())}")
    # for y in range(2020, 2030):
    #     print(f"---------{y}---------")
    #     print(f"법인세 차감전 순이익 {int_format(d.법인세비용차감전순이익(y))}")
    #     print(f"매출액 {int_format(d.매출액(y))} 매출원가 {int_format(d.매출원가(y))} 영업이익 {int_format(d.영업이익(y))} "
    #           f"영업이익률 {int_format(d.영업이익(y) / d.매출액(y) )}")
    #     print(f"주주환원율 {int_format(d.주주환원율(y))}")
    #     print(f"당기순이익 {int_format(d.당기순이익(y))} 주주환원 {int_format(d.주주환원(y))} 영업이익 {int_format(d.영업이익(y))} 지분법손익 {int_format(d.지분법손익(y))} 금융손익 {int_format(d.금융손익(y))} 기타손익 {int_format(d.기타손익(y))} 법인세비용 {int_format(d.법인세비용(y))}")
    # d = DartTicker("035420")
    # print(d.info())
