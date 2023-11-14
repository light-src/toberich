# https://purplechip.tistory.com/31
from wics import qconfig
import requests
from pandas import DataFrame
from slack_finance_response import usable_ticker
import statistics

if __name__ == '__main__':
    df = DataFrame(columns=['code', 'name', 'ls', 'ms'])
    date = '20231113'
    # there is no data in the stock market closed day and before market open.
    # weekends, Jan 1, Dec 31 etc

    for wics_code in qconfig.wics_mc.keys():
        response = requests.get(qconfig.wics_url(date, wics_code))

        if response.status_code == 200:  # request success
            json_list = response.json()  # dictionary
            주주환원율_list = []
            # response.text -> return str type
            for json in json_list['list']:
                ls = json['SEC_NM_KOR']  # Large sector
                ms = json['IDX_NM_KOR'][5:]  # Medium sector
                code = json['CMP_CD']  # Company code
                name = json['CMP_KOR']  # Company korean name
                print({'code': code, 'name': name, 'ls': ls, 'ms': ms})
                tt = usable_ticker(code+".ks")
                주주환원율 = tt.평균주주환원율()
                print(f"company:{name}, 주주환원율: {주주환원율}")
                주주환원율_list.append(주주환원율)
            print(f"sector: {wics_code}, median: {statistics.median(주주환원율_list)}")
