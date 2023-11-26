from wics import const, wics
from slack_util import send_slack, dict_slack_content_to_blocks, list_dict_slack_content_to_blocks


def send_slack_wics_lc(channel):
    lc = const.wics_lc
    send_slack(
        dict_slack_content_to_blocks(
            f"🏢 Wics Large Sector 🏢\n",
            lc.keys(),
            lc),
        channel
    )


def send_slack_wics_mc(channel):
    mc = const.wics_mc
    send_slack(
        dict_slack_content_to_blocks(
            f"🏢 Wics Medium Sector 🏢\n",
            mc.keys(),
            mc),
        channel
    )


def send_slack_wics_code(code, channel):
    w = wics.Wics()
    companies = w.get_companies(code)
    send_slack(
        list_dict_slack_content_to_blocks(
            f"🏢 Wics {code} 🏢\n",
            companies
        ),
        channel
    )


def send_slack_response(txt, channel):
    if txt == 'lc':
        send_slack_wics_lc(channel)
    elif txt == 'mc':
        send_slack_wics_mc(channel)
    else:
        send_slack_wics_code(txt, channel)


if __name__ == "__main__":
    ticker = "META"
    year = 2022
    channel = "C06486XKLVA"
    # send_slack_wics_lc()
    # send_slack_wics_mc()
    send_slack_wics_code("10")