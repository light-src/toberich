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

    return jsonify(ticker.info())


@app.get('/financial_info')
def financial_info():
    request_ticker = request.args.get('ticker')
    request_year = request.args.get('year')

    if request_ticker is None:
        return "ticker 가 누락되었습니다.", 400

    if request_year is None:
        return "year 가 누락되었습니다.", 400

    ticker = yticker.YTicker(request_ticker)

    return jsonify(ticker.financial_info(int(request_year)))


if __name__ == '__main__':
    app.run(debug=True)
