from wics import const
import requests
from datetime import datetime, timedelta
from ticker_util import usable_ticker


class Wics:
    def get_lc(self):
        return const.wics_lc

    def get_mc(self):
        return const.wics_mc

    def get_companies(self, code):
        date = self._get_date()
        response = requests.get(const.wics_url(date, code))
        result = []

        if response.status_code == 200:  # request success
            json_list = response.json()  # dictionary
            for e in json_list['list']:
                # ls = e['SEC_NM_KOR']  # Large sector
                # ms = e['IDX_NM_KOR'][5:]  # Medium sector
                code = e['CMP_CD']  # Company code
                name = e['CMP_KOR']  # Company korean name
                try:
                    할인율 = usable_ticker(f'{code}.ks').예상할인율()
                except Exception as e:
                    할인율 = f"Cannot Calculate"
                result.append({'company': name, 'code': code, '할인율': 할인율})
        else:
            raise f"get company error: {response.status_code}"

        return result

    def _get_date(self):
        # 현재 날짜 및 시간 가져오기
        now = datetime.now()

        # 요일 확인 (0: 월요일, 1: 화요일, ..., 6: 일요일)
        weekday = now.weekday()

        # 만약 오늘이 토요일이나 일요일이라면
        if weekday == 5:
            day = now - timedelta(days=1)
        elif weekday == 6:
            day = now - timedelta(days=2)
        else:
            day = now

        # 원하는 형식으로 현재 날짜 포맷팅
        formatted_date = day.strftime("%Y%m%d")

        return formatted_date


if __name__ == '__main__':
    wics = Wics()
    # print(wics.get_mc())
    # print(wics.get_lc())
    usable_ticker(f'046120.ks').예상할인율()
