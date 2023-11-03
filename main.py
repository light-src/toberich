import yfinance

import yticker

if __name__ == '__main__':
    tt = yticker.YTicker("000270.KS")
    print("--------Ticker---------")
    print(tt)
    print("-----------------")
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
    for year in years:
        print("--------" + str(year) + "---------")
        print(tt.string(year))
        print("-----------------")
    # tt = yfinance.Ticker("000270.KS")
    # print(tt.cashflow.get('2021-12-31'))
