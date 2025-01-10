import api.fetch as api
import math

config = api.get_settings()

"""
Format your strategies responses as a dict with the values you need.

Example:

response = {
    "buy": True,
    "price": current_candle["open"],
    "amount": config["account"]["baseOrderValue"],
}
"""
