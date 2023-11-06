from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

from chatgpt import ChatGPT


def send_slack(text: str, channel):
    token = os.getenv("SLACK_API_TOKEN")
    client = WebClient(token=token)
    try:
        client.chat_postMessage(
            channel=channel,
            blocks=[
                {
                    "type": "divider"
                },
                {
                    "type": "mkrdwn",
                    "text": text.strip()
                },
                {
                    "type": "divider"
                }
            ]
        )
    except SlackApiError as e:
        print(f"Error: {e}")


def send_gpt_response(inquire: str, channel: str):
    token = os.getenv("OPEN_API_TOKEN")
    send_slack(
        ChatGPT(inquire, token),
        channel
    )

