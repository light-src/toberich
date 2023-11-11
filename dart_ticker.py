import os

import ticker
import OpenDartReader
import dart_terms
import pandas as pd
import FinanceDataReader as fdr


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
        self._cache = {}
        self.ticker = tt
        self.dart = OpenDartReader(api_key)

    def can_use(self) -> bool:
        if not self.ticker.endswith(".ks"):
            return False
        try:
            self.손익계산서(2022)
        except KeyError:
            return False
        return True

    def first_year(self) -> int:
        min = 2015
        return min

    def _매출액(self, year):
        return self._손익계산서(dart_terms.매출액, year)

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
        return float(value)

    def _재무상태표(self, index, year):
        try:
         value = self.재무상태표(year).loc[index]
        except KeyError:
            value = 0
        return float(value)

    def _현금흐름표(self, index, year):
        try:
         value = self.현금흐름표(year).loc[index]
        except KeyError:
            value = 0
        if value == '':
            value = 0
        return float(value)

    def 손익계산서(self, year):
        return self._재무제표("손익계산서", year)[0]

    def 재무상태표(self, year):
        return self._재무제표("재무상태표", year)[0]

    def 현금흐름표(self, year):
        return self._재무제표("현금흐름표", year)[0]

    def _재무제표(self, elem, year):
        key = str(elem) + str(year)
        if self._cache.get(key) is not None:
            return self._cache.get(key)
        tt = self.ticker.replace(".ks", "")
        df = self.dart.finstate_all(tt, year)
        raw = df[df['sj_nm'] == elem]
        keys = raw['account_nm'].tolist()
        values = raw['thstrm_amount'].tolist()
        self._cache[key] = pd.DataFrame(values, index=keys)
        return self._cache[key]


if __name__ == "__main__":
    d = DartTicker("삼성전자").손익계산서(2022)
    print(d.index)
    print(d)