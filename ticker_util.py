import dart_ticker
import yticker


def usable_ticker(tt):
    candidates = [dart_ticker.DartTicker, yticker.YTicker]
    for candidate in candidates:
        try:
            candidate_ticker = candidate(tt)
        except Exception:
            continue

        if candidate_ticker.can_use():
            return candidate_ticker

    raise Exception("cannot find usable ticker type")