import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from flask import jsonify

def int_format(value):
    if is_float(value):
        value = float(value)
    if isinstance(value, float):
        return format(value, ",")
    if value == "":
        value = "-"
    return str(value)


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
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


def default_block(title) -> list:
    return [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title,
                "emoji": True
            }
        },
    ]


def dict_slack_content_to_blocks(title, keys, values):
    block = default_block(title)

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


def list_dict_slack_content_to_blocks(title, elements):
    block = default_block(title)

    for element in elements:
        values = element.values()
        block.append({
            "type": "section",
            "fields": [{"type": "mrkdwn", "text": str(value)} for value in values]
        })

    return [block[i:i + 40] for i in range(0, len(block), 40)]
