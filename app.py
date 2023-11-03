import yticker
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


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
