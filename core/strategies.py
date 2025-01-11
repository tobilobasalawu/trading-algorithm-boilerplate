import api.fetch as api
import math
import numpy as np

config = api.get_settings()

def momentum_reversion_strategy(candles):
    """
    Implements a momentum-reversion hybrid strategy.
    """
    # Calculate moving averages
    short_window = 10
    long_window = 50
    mean_window = 20

    # Initialize signals
    signals = {
        "buy": False,
        "sell": False,
        "price": None,
        "amount": config["account"]["baseOrderValue"],
    }

    # Calculate moving averages and mean
    closes = [candle["close"] for candle in candles]
    sma_short = np.mean(closes[-short_window:]) if len(closes) >= short_window else None
    sma_long = np.mean(closes[-long_window:]) if len(closes) >= long_window else None
    mean_price = np.mean(closes[-mean_window:]) if len(closes) >= mean_window else None

    # Generate buy/sell signals
    if sma_short is not None and sma_long is not None:
        if sma_short > sma_long:  # Momentum Buy Signal
            signals["buy"] = True
            signals["price"] = candles[-1]["open"]  # Use the current candle's open price
        elif sma_short < sma_long:  # Momentum Sell Signal
            signals["sell"] = True
            signals["price"] = candles[-1]["open"]

    # Mean Reversion Logic
    if mean_price is not None:
        if closes[-1] < mean_price * 0.95:  # Buy if price is significantly below mean
            signals["buy"] = True
            signals["price"] = candles[-1]["open"]
        elif closes[-1] > mean_price * 1.05:  # Sell if price is significantly above mean
            signals["sell"] = True
            signals["price"] = candles[-1]["open"]

    return signals

"""
Format your strategies responses as a dict with the values you need.

Example:

response = {
    "buy": True,
    "price": current_candle["open"],
    "amount": config["account"]["baseOrderValue"],
}
"""
