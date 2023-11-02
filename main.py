import yticker
import yfinance as yf
import terms


def print_ticker(company):
    print_years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]

    tk = ticker.YTicker(company)
    tk.set_use_non_growth_threshold(True)
    print(tk)
    for year in print_years:
        print("---------------------------------------")
        print("------------" + str(year) + "년도 재무정보 ------------")
        print("---------------------------------------")
        print(tk.string(year))


if __name__ == '__main__':
    print_ticker("213500.KS")
    # meta = yf.Ticker('323410.KS')
    # print(meta.cashflow.index)
