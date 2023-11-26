# https://purplechip.tistory.com/31
import time

import const
import requests
from pandas import DataFrame
from ticker_util import usable_ticker
import threading

companies = []


def print_company(company: dict):
    ls = company['SEC_NM_KOR']  # Large sector
    ms = company['IDX_NM_KOR'][5:]  # Medium sector
    code = company['CMP_CD']  # Company code
    name = company['CMP_KOR']  # Company korean name

    try:
        print({'code': code, 'name': name, 'ls': ls, 'ms': ms})
        tt = usable_ticker(code + ".ks")
        예상할인율 = tt.예상할인율()
        companies.append({'company': name, 'code': code, '예상할인율': 예상할인율})
    except Exception:
        print(f"---------- failed company : {name}")
        pass


def print_code(code):
    response = requests.get(const.wics_url(date, code))

    if response.status_code == 200:  # request success
        json_list = response.json()  # dictionary
        cnt = len(json_list['list'])
        # response.text -> return str type
        for json in json_list['list']:
            thread = threading.Thread(
                target=print_company,
                args=[json]
            )
            thread.start()

        time.sleep(45)

        print(f"--------------------------------------------------------------")
        print(f"--------------------------------------------------------------")
        for company in companies:
            print(company)


if __name__ == '__main__':
    df = DataFrame(columns=['code', 'name', 'ls', 'ms'])
    date = '20231113'
    # there is no data in the stock market closed day and before market open.
    # weekends, Jan 1, Dec 31 etc

    for wics_code in const.wics_mc.keys():
        print_code(10)

    # print(f"--------------------------------------------------------------")
    # print(f"--------------------------------------------------------------")
    # print(f"sector: {wics_code}, median: {statistics.median(예상할인율_list)}")
    # average = sum(예상할인율_list) / len(예상할인율_list)
    # print(f"sector: {wics_code}, average: {average}")
    # print(f"--------------------------------------------------------------")
    # print(f"--------------------------------------------------------------")
