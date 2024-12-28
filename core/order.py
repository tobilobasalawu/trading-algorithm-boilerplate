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
    - data.rsi: A list of RSI values.
    - data.sma: A list of SMA values.
    - data.atr: A list of ATR values.
    - data.std_dev: A list of standard deviation values.

    All these values line up for each of your candles. For example, if you took datetimes[6], 
    closes[6] and account.rsi[6], each value would correlate to the same candle; the 7th candle.
    """

    # <==================== Add your custom indicator logic below ====================>

    candles = []
    for i in range(len(data.closes) - data.max_period):
        candle = {}
        candle["datetime"] = datetimes[i]
        candle["open"] = opens[i]
        candle["close"] = closes[i]
        candle["high"] = highs[i]
        candle["low"] = lows[i]
        candle["sma"] = data.sma[i]
        candle["rsi"] = data.rsi[i]
        candle["atr"] = data.atr[i]
        candle["std_dev"] = data.std_dev[i]

        candles.append(candle)
        # iterate through the candles. It doesn't matter which value you use (rsi, datetimes, opens, closes, highs, lows) as all these lists are the same length.
        # One value from each of these lists makes up the data needed to render 1 candle.

    for i in range(len(candles)):
        if candles[i]["rsi"] < 30:
            entries = indicator.add(
                entries, candles[i]["datetime"], candles[i]["close"]
            )
            account.buy_order(
                candles[i]["datetime"], config["baseOrderValue"], candles[i]["close"]
            )
            log.append("BUY")
        elif candles[i]["rsi"] > 70 and log[-1] == "BUY":
            exits = indicator.add(exits, candles[i]["datetime"], candles[i]["close"])
            account.sell_order(candles[i]["datetime"], candles[i]["close"])
            log.append("SELL")

        account.open_position_amount = account.shares_owned * candles[i]["close"]
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
