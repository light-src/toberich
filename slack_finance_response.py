from slack_util import send_slack, dict_slack_content_to_blocks
import dart_ticker
import yticker


def send_slack_info(ticker, channel):
    tt = usable_ticker(ticker)
    send_slack(
        dict_slack_content_to_blocks(
            f"🏢 {ticker} info 🏢\n",
            tt.info().keys(),
            tt.info()),
        channel
    )


def send_slack_financial_info(ticker: str, year: int, channel: str):
    tt = usable_ticker(ticker)
    send_slack(
        dict_slack_content_to_blocks(
            f"💸 {year} {ticker} info 💸\n",
            tt.financial_info(year).keys(),
            tt.financial_info(year)
        ),
        channel
    )


def send_slack_incomestmt(ticker: str, year: int, channel: str):
    tt = usable_ticker(ticker)
    send_slack(
        dict_slack_content_to_blocks(
            f"💸 {year} {ticker} income sheet 💸\n",
            tt.손익계산서(year).index,
            tt.손익계산서(year)
        ),
        channel
    )


def send_slack_balancesheet(ticker: str, year: int, channel: str):
    tt = usable_ticker(ticker)
    send_slack(
        dict_slack_content_to_blocks(
            f"📁 {year} {ticker} balance sheet 📁\n",
            tt.재무상태표(year).index,
            tt.재무상태표(year)
        ),
        channel
    )


def send_slack_cashflow(ticker: str, year: int, channel: str):
    tt = usable_ticker(ticker)
    send_slack(
        dict_slack_content_to_blocks(
            f"📁 {year} {ticker} cashflow 📁\n",
            tt.현금흐름표(year).index,
            tt.현금흐름표(year)
        ),
        channel
    )


def usable_ticker(tt):
    candidates = [dart_ticker.DartTicker, yticker.YTicker]
    for candidate in candidates:
        try:
            candidate_ticker = candidate(tt)
        except Exception:
            continue

        if candidate_ticker.can_use():
            return candidate_ticker

    raise Exception("cannot find usable ticker type")


if __name__ == "__main__":
    ticker = "005930.ks"
    year = 2022
    channel = "C06486XKLVA"
    send_slack_info(ticker, channel)
    send_slack_financial_info(ticker, year, channel)
    send_slack_incomestmt(ticker, year, channel)
    send_slack_balancesheet(ticker, year, channel)
    send_slack_cashflow(ticker, year, channel)
