import json

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import dart_ticker
import yticker
import os

from flask import jsonify


def int_format(value):
    if is_float(value):
        value = float(value)
    if isinstance(value, float):
        return format(value, ",")
    return str(value)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def slack_response(text):
    return jsonify({
        "response_type": "in_channel",  # "in_channel" or "ephemeral"
        "text": text,
    })


def send_slack(blocks, channel):
    token = os.getenv("SLACK_API_TOKEN")
    client = WebClient(token=token)
    try:
        client.chat_postMessage(
            channel=channel,
            blocks=[{
                "type": "divider"
            }]
        )
        for block in blocks:
            req = json.dumps(block)
            client.chat_postMessage(
                channel=channel,
                mkrdwn=True,
                blocks=req)
        client.chat_postMessage(
            channel=channel,
            blocks=[{
                "type": "divider"
            }]
        )
    except SlackApiError as e:
        print(f"Error: {e}")


def dict_slack_content_to_blocks(title, keys, values):
    block = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title,
                "emoji": True
            }
        },
    ]

    for key in keys:
        block.append({
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*{key}*"
                },
                {
                    "type": "mrkdwn",
                    "text": int_format(values[key])
                }
            ]
        })

    return [block[i:i + 40] for i in range(0, len(block), 40)]


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
        candidate_ticker = candidate(tt)
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
