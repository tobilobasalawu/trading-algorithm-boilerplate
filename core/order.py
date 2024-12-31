import utils.convert as convert
import pandas as pd
import core.Account as order
import utils.indicator as indicator
import api.fetch as api
from core.Rules import Rules
import core.strategies as strategies


def indicators(account, data):
    config = api.get_settings()
    entries = {}  # datetime: close price
    exits = {}  # datetime: close price
    log = [-1]

    decisions = {
        "strategy_1": {
            "call": "HOLD",
            "weight": config["strategyWeights"]["strategy1"],
        },
        "strategy_2": {
            "call": "HOLD",
            "weight": config["strategyWeights"]["strategy2"],
        },
        "strategy_3": {
            "call": "HOLD",
            "weight": config["strategyWeights"]["strategy3"],
        },
    }

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

    candles = []
    for i in range(len(data.closes)):
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

    def buy(entries, amount):
        entries = indicator.add(entries, candles[i]["datetime"], candles[i]["close"])
        account.buy_order(candles[i]["datetime"], amount, candles[i]["close"])
        log.append("BUY")

    def sell(exits):
        exits = indicator.add(exits, candles[i]["datetime"], candles[i]["close"])
        account.sell_order(candles[i]["datetime"], candles[i]["close"])
        log.append("SELL")

    # <==================== Add your custom indicator logic below ====================>

    """
    Place a buy order:
    buy(entries, amount)

    Place a sell order:
    sell(entries)
    """

    initial_buy_amount = config["baseOrderValue"] * config["buyMultiplier"]
    payload = {
        "z": 0,
        "initial_buy_amount": 0,
        "uninvested_balance": account.uninvested_balance,
    }
    rules = Rules(payload)

    for i in range(len(candles)):

        # Strategy 1
        strategy_1_response = strategies.ma_below_close_price()

        # Strategy 2
        strategy_2_response = 0

        # Strategy 3
        strategy_3_response = 0

        # ======================================

        z = strategy_1_response + strategy_2_response + strategy_3_response

        payload = {
            "initial_buy_amount": initial_buy_amount,
            "uninvested_balance": account.uninvested_balance,
        }
        rules.payload = payload

        response = rules.balance_valid()

        # Logic for placing buy and sell orders
        if response["valid"] == True:
            pass

        # <==================== Add your custom indicator logic above ====================>

        # Logic for updating balance:

        account.open_position_amount = account.shares_owned * candles[i]["close"]
        account.balance_absolute = (
            account.uninvested_balance + account.open_position_amount
        )
        account.profit = account.balance_absolute - config["initialBalance"]

        data.ongoing_balance.append(account.balance_absolute)

    entries = pd.Series(entries.values(), index=entries.keys())
    exits = pd.Series(exits.values(), index=exits.keys())

    return entries, exits
