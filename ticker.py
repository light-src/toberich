from abc import ABC, abstractmethod


class Ticker(ABC):
    ticker = ""

    @abstractmethod
    def 손익계산서(self, year):
        pass

    @abstractmethod
    def 재무상태표(self, year):
        pass

    @abstractmethod
    def 현금흐름표(self, year):
        pass

    @abstractmethod
    def 원본데이터(self, year):
        pass
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

    @abstractmethod
    def 당기순이익(self, year):
        pass

    @abstractmethod
    def 주주환원(self, year):
        pass

    @abstractmethod
    def 평균주주환원율(self):
        pass

    @abstractmethod
    def 주주환원율(self, year):
        pass

    @abstractmethod
    def 예상할인율(self):
        pass

    @abstractmethod
    def 시가총액(self):
        pass

    @abstractmethod
    def 리스크프리미엄(self):
        return self.예상할인율() - self.국채수익률

    @property
    def 국채수익률(self):
        pass

    def info(self):
        return {
            "Ticker": self.ticker,
            "Market Cap": self.시가총액(),
            "Avg RevenueGrowth Rate": self.평균매출액증가율(),
            "Expected Discount Rate": self.예상할인율(),
            "Avg Shareholder Yield": -1 * self.평균주주환원율(),
            "Risk Premium": self.리스크프리미엄(),
        }

    def financial_info(self, year):
        return {
            "Original Data": self.원본데이터(year),
            "Total Revenue": self.매출액(year),
            "Cost Of Revenue": self.매출원가(year),
            "Gross Profit": self.매출총이익(year),
            "SG&A": self.판매비와관리비(year),
            "Operating Income": self.영업이익(year),
            "Equity Method Income": self.지분법손익(year),
            "Net Interest Income": self.금융손익(year),
            "Other Income": self.기타손익(year),
            "Pretax Income": self.법인세비용차감전순이익(year),
            "Tax Provision": self.법인세비용(year),
            "Net Income": self.당기순이익(year),
            "Shareholder Yield": -1 * self.주주환원율(year),
            "Shareholder Return": -1 * self.주주환원(year)
        }
