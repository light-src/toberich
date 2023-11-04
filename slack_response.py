from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

import yticker
from flask import jsonify


def slack_response(text):
    return jsonify({
        "response_type": "in_channel",  # "in_channel" or "ephemeral"
        "text": text,
    })


def send_slack(msg, channel):
    token = os.getenv("SLACK_API_TOKEN")
    try:
        client = WebClient(token=token)
        client.chat_postMessage(
            channel=channel,
            mkrdwn=True,
            text=msg)
    except SlackApiError as e:
        print(f"Error: {e}")


def send_slack_info(ticker, channel):
    ticker = yticker.YTicker(ticker)
    send_slack(ticker.info_slack_str(), channel)


def send_slack_financial_info(ticker: str, year: int, channel: str):
    ticker = yticker.YTicker(ticker)
    send_slack(ticker.financial_info_slack_str(year), channel)


if __name__ == "__main__":
    send_slack_info("META", "C06486XKLVA")
    send_slack_financial_info("META", 2022, "C06486XKLVA")

