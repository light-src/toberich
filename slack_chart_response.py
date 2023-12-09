import re

from slack_util import send_image
from ticker_util import usable_ticker
from chart import Chart

color = ['b', 'g', 'r', 'c', 'm', 'y']

def get_chart(ticker, expressions) -> Chart:
    tt = usable_ticker(ticker)
    chart = Chart(ticker)
    chart.set_x(list(range(tt.first_year(), tt.this_year)))
    for i in range(len(expressions)):
        calculated = calculate_expression(tt, expressions[i])
        chart.add_elements(calculated, 'r', expressions[i])
    return chart


def calculate_expression(tt, expression) -> list:
    pattern = r"'(.*?)'"
    accounts = re.findall(pattern, expression)

    acc_map = {}
    length = 0
    for account in accounts:
        acc_map[account] = tt.account(account)
        length = len(acc_map[account])

    expression_list = [expression] * length
    for i in range(len(expression_list)):
        for account in accounts:
            expression_list[i] = expression_list[i].replace(account, str(acc_map[account][i]))

    result_list = []
    for exp in expression_list:
        exp = exp.replace("'", "")
        result_list.append(eval(exp))

    return result_list


def send_slack_response(req_txt, channel):
    txts = req_txt.split(" ", maxsplit=1)
    ticker = txts[0]
    exps = txts[1].split(",")
    path = get_chart(ticker, exps).save_image(req_txt)
    send_image(ticker, path, channel)


def validate_expressions(txt):
    txts = txt.split(" ", maxsplit=1)
    exps = txts[1].split(",")
    if len(exps) > 6:
        return False
    return True


if __name__ == '__main__':
    send_slack_response("MO 'Pretax Income' - 'Net Income', 'Other Income Expense'", 1234)
