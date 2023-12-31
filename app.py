import slack_finance_response
import slack_gpt_response
import slack_wics_response
import slack_chart_response
import slack_util

import threading
import db
from flask import Flask, request, json


app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False


@app.post('/slack/info')
def slack_info():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')
    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #ticker")

    request_ticker = text.split(" ")[0]
    thread = threading.Thread(target=slack_finance_response.send_slack_info, args=[request_ticker, channel_id])
    thread.start()
    return slack_util.slack_response(f"request ${request_ticker} received")


@app.post('/slack/financial_info')
def slack_financial_info():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_finance_response.send_slack_financial_info,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/incomestmt')
def slack_incomestmt():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_finance_response.send_slack_incomestmt,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/balancesheet')
def slack_balancesheet():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_finance_response.send_slack_balancesheet,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/cashflow')
def slack_cashflow():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_util.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_finance_response.send_slack_cashflow,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/gpt')
def slack_gpt():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have #inquire")

    thread = threading.Thread(
        target=slack_gpt_response.send_gpt_response,
        args=[text, channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request received")


@app.post('/slack/wics')
def slack_wics():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response("invalid input, test must have lc or mc or #code")

    thread = threading.Thread(
        target=slack_wics_response.send_slack_response,
        args=[text, channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request received")


@app.post('/slack/graph')
def slack_graph():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_util.slack_response(f"invalid input : {text}")

    if not slack_chart_response.validate_expressions(text):
        return slack_util.slack_response(f"invalid input. max expression - 6 : {text}")

    thread = threading.Thread(
        target=slack_chart_response.send_slack_response,
        args=[text, channel_id]
    )
    thread.start()
    return slack_util.slack_response(f"request received")


if __name__ == '__main__':
    db = db.SQLiteDatabase()
    db.create_table_if_not_exists()
    db.close_connection()

    app.run(debug=True, port=8080, host='0.0.0.0')
