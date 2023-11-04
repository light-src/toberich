from abc import ABC, abstractmethod


def row_format(key, value):
    if isinstance(value, float):
        value = int_format(value)
    return f"{key: <20} {value: <50}\n"


def int_format(value):
    return format(value, ",")


class Ticker(ABC):
    ticker = ""

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
            "시가총액": self.시가총액(),
            "평균 매출액 증가율": self.평균매출액증가율(),
            "예상할인율": self.예상할인율(),
            "평균주주환원율": -1 * self.평균주주환원율(),
            "리스크 프리미엄": self.리스크프리미엄(),
        }

    def financial_info(self, year):
        return {
            "원본데이터": self.원본데이터(year),
            "매출액": self.매출액(year),
            "매출원가": self.매출원가(year),
            "매출총이익": self.매출총이익(year),
            "판관비": self.판매비와관리비(year),
            "영업이익": self.영업이익(year),
            "지분법손익": self.지분법손익(year),
            "금융손익": self.금융손익(year),
            "기타손익": self.기타손익(year),
            "법인세비용차감전순이익": self.법인세비용차감전순이익(year),
            "법인세비용": self.법인세비용(year),
            "당기순이익": self.당기순이익(year),
            "주주환원율": -1 * self.주주환원율(year),
            "주주환원": -1 * self.주주환원(year)
        }

    def info_str(self):
        info = ""
        info_dict = self.info()
        for key in info_dict:
            info += row_format(key, info_dict[key])

        return f"🏢 *{self.ticker}정보* 🏢\n" \
            + info

    def financial_info_str(self, year):
        info = ""
        info_dict = self.financial_info(year)
        for key in info_dict:
            info += row_format(key, info_dict[key])

        return f" 💸 *{year}년도 {self.ticker}정보* 💸\n" \
            + info
