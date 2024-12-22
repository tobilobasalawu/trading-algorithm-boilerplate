import utils.convert_series as convert
import pandas as pd
import core.Account as order
import utils.indicator as indicator
import api.fetch as api


def indicators(account, data_obj, rsi):
    config = api.get_settings()
    entries = {}  # datetime: close price
    exits = {}  # datetime: close price
    log = [-1]

    datetimes, opens, closes, highs, lows = convert.series_to_lists(data_obj)

    for i in range(len(rsi)):
        if rsi[i] < 30 and log[-1] != "BUY":
            entries = indicator.add(entries, datetimes[i], closes[i])

            account.buy_order(config["baseOrderValue"], closes[i])

            log.append("BUY")
        elif rsi[i] > 70 and log[-1] != "SELL" and "BUY" in log:
            exits = indicator.add(exits, datetimes[i], closes[i])

            account.sell_order(closes[i])

            log.append("SELL")
        else:
            continue

    entries = pd.Series(entries.values(), index=entries.keys())
    exits = pd.Series(exits.values(), index=exits.keys())

    return entries, exits
