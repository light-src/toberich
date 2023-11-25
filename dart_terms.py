import os

import ticker
import OpenDartReader
import pandas as pd

# 손익계산서
매출액 = "매출액"
수익매출액 = "수익(매출액)"
매출원가 = "매출원가"
매출총이익 = "매출총이익"
판매비와관리비 = "판매비와관리비"
영업이익 = "영업이익"
지분법수익 = "지분법이익"
지분법비용 = "지분법비용"
금융수익 = "금융수익"
금융비용 = "금융비용"
기타수익 = "기타수익"
기타비용 = "기타비용"
법인세비용차감전순이익 = "법인세비용차감전순이익(손실)"
법인세비용 = "법인세비용"
당기순이익 = "당기순이익(손실)"

# 현금흐름표
자기주식의취득 = "자기주식의 취득"
배당금의지급 = "배당금의 지급"