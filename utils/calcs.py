import utils.convert_series as convert
import pandas as pd


def indicators(data_obj, rsi):
    entries = {}  # datetime: close price
    exits = {}  # datetime: close price

    datetimes, opens, closes, highs, lows = convert.series_to_lists(data_obj)

    for i in range(len(rsi)):
        if rsi[i] < 30:
            entries[datetimes[i]] = closes[i]
        elif rsi[i] > 70:
            exits[datetimes[i]] = closes[i]
        else:
            continue

    entries = pd.Series(entries.values(), index=entries.keys())
    exits = pd.Series(exits.values(), index=exits.keys())

    return entries, exits
