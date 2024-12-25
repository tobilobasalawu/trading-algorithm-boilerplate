import utils.convert as convert
import pandas as pd
import core.Account as order
import utils.indicator as indicator
import api.fetch as api


def indicators(account, data):
    config = api.get_settings()
    entries = {}  # datetime: close price
    exits = {}  # datetime: close price
    log = [-1]

    datetimes, opens, closes, highs, lows = convert.series_to_lists(data)

    """
    Here is a list of the data you have access to:

    - datetimes: A list of all datetimes.
    - opens: A list of opening prices.
    - closes: A list of closing prices.
    - highs: A list of high prices.
    - lows: A list of low prices.
    - account.rsi: A list of RSI values.
    - account.sma: A list of SMA values.

    All these values line up for each of your candles. For example, if you took datetimes[6], 
    closes[6] and account.rsi[6], each value would correlate to the same candle; the 7th candle.
    """

    # <==================== Add your custom indicator logic below ====================>

    for i in range(len(data.closes) - data.max_period):
        # iterate through the candles. It doesn't matter which value you use (rsi, datetimes, opens, closes, highs, lows) as all these lists are the same length.
        # One value from each of these lists makes up the data needed to render 1 candle.

        if data.rsi[i] < 30:
            entries = indicator.add(entries, datetimes[i], closes[i])
            account.buy_order(datetimes[i], config["baseOrderValue"], closes[i])
            log.append("BUY")
        elif data.rsi[i] > 70 and log[-1] == "BUY":
            exits = indicator.add(exits, datetimes[i], closes[i])
            account.sell_order(datetimes[i], closes[i])
            log.append("SELL")

        account.open_position_amount = account.shares_owned * closes[i]
        account.balance_absolute = (
            account.uninvested_balance + account.open_position_amount
        )
        account.profit = account.balance_absolute - config["initialBalance"]

        data.ongoing_balance.append(account.balance_absolute)

        # Adds a buy/sell signal if the RSI drops below/reaches a certain value

    # <==================== Add your custom indicator logic above ====================>

    entries = pd.Series(entries.values(), index=entries.keys())
    exits = pd.Series(exits.values(), index=exits.keys())

    return entries, exits
