import slack_response
import threading
from flask import Flask, request, json


app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False


@app.post('/slack/info')
def slack_info():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')
    if not isinstance(text, str):
        return slack_response.slack_response("invalid input, test must have #ticker")

    request_ticker = text.split(" ")[0]
    thread = threading.Thread(target=slack_response.send_slack_info, args=[request_ticker, channel_id])
    thread.start()
    return slack_response.slack_response(f"request ${request_ticker} received")


@app.post('/slack/financial_info')
def slack_financial_info():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_response.send_slack_financial_info,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_response.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/incomestmt')
def slack_incomestmt():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_response.send_slack_incomestmt,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_response.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/balancesheet')
def slack_balancesheet():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_response.send_slack_balancesheet,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_response.slack_response(f"request ${request_ticker} ${request_year} received")


@app.post('/slack/cashflow')
def slack_cashflow():
    data = request.form
    text = data.get('text')
    channel_id = data.get('channel_id')

    if not isinstance(text, str):
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    split = text.split(" ")
    if len(split) < 2:
        return slack_response.slack_response("invalid input, test must have #ticker #year")

    request_ticker = split[0]
    request_year = split[1]
    thread = threading.Thread(
        target=slack_response.send_slack_cashflow,
        args=[request_ticker, int(request_year), channel_id]
    )
    thread.start()
    return slack_response.slack_response(f"request ${request_ticker} ${request_year} received")


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
