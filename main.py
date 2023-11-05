import yfinance

import yticker

if __name__ == '__main__':
    tt = yticker.YTicker("323410.ks")
    print("--------Ticker---------")
    print(tt.info())
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
    for year in years:
        print(tt.financial_info(year))
    # tt = yfinance.Ticker("000270.KS")
    # print(tt.cashflow.get('2021-12-31'))
