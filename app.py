import slack_response
import yticker
import threading
from flask import Flask, request, json, jsonify


app = Flask(__name__)
json.provider.DefaultJSONProvider.ensure_ascii = False


@app.get('/info')
def info():
    request_ticker = request.args.get('ticker')

    if request_ticker is None:
        return "ticker 가 누락되었습니다.", 400

    ticker = yticker.YTicker(request_ticker)

    try:
        return jsonify(ticker.info())
    except Exception as e:
        return e, 500


@app.get('/financial_info')
def financial_info():
    request_ticker = request.args.get('ticker')
    request_year = request.args.get('year')

    if request_ticker is None:
        return "ticker 가 누락되었습니다.", 400

    if request_year is None:
        return "year 가 누락되었습니다.", 400

    ticker = yticker.YTicker(request_ticker)

    try:
        return jsonify(ticker.financial_info(int(request_year)))
    except Exception as e:
        return e, 500


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


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
