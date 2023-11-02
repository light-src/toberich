from abc import ABC, abstractmethod
import calculator


class Ticker(ABC):

    @abstractmethod
    def 매출액(self, year):
        pass

    @abstractmethod
    def 평균매출액증가율(self):
        pass

    @abstractmethod
    def 매출원가(self, year):
        pass

    @abstractmethod
    def 평균매출원가율(self):
        pass

    @abstractmethod
    def 매출총이익(self, year):
        pass

    @abstractmethod
    def 판매비와관리비(self, year):
        pass

    @abstractmethod
    def 매출액대비판관비율(self):
        pass

    @abstractmethod
    def 영업이익(self, year):
        pass

    @abstractmethod
    def 지분법손익(self, year):
        pass

    @abstractmethod
    def 금융손익(self, year):
        pass

    @abstractmethod
    def 기타손익(self, year):
        pass

    @abstractmethod
    def 법인세비용차감전순이익(self, year):
        pass

    @abstractmethod
    def 법인세비용(self, year):
        pass

    @abstractmethod
    def 평균유효세율(self):
        pass

    def 당기순이익(self, year) -> float:
        return self.법인세비용차감전순이익(year) - self.법인세비용(year)

    @abstractmethod
    def 주주환원(self, year):
        pass

    @abstractmethod
    def 주주환원율(self, year):
        pass

    def 예상할인율(self) -> float:
        cashflow = [-1 * self.시가총액()] + [-1 * self.주주환원(y) for y in range(2020, 2060)]
        return calculator.irr(cashflow)

    @abstractmethod
    def 시가총액(self):
        pass

    @abstractmethod
    def 리스크프리미엄(self):
        return self.예상할인율() - self.국채수익률()

    @abstractmethod
    def 국채수익률(self):
        pass
