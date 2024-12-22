import utils.indicator as indicator
import api.fetch as api

config = api.get_settings()


class Account:
    def __init__(self, balance, base_order_value, orders, profit, volume):
        self.balance = balance  # Initial balance
        self.base_order_value = base_order_value  # percentage of total balance
        # e.g. 10 = minimum of 10% of account balance put into each trade
        self.orders = (
            orders  # List of dicts: order amount, buy/sell price, units bought
        )
        self.profit = profit
        self.volume = volume

    def buy_order(self, order_value, stock_price):  # Place an order
        order = {
            "type": "BUY",
            "amount": order_value,
            "price": stock_price,
            "units": order_value / stock_price,
        }
        self.balance -= order["amount"]
        self.volume += order["amount"]
        self.orders.append(order)

        """
        print(
            "\n=====================================================================================\n"
        )
        print(
            f"Bought ${order_value:.2f} of {config["ticker"]} at ${stock_price:.2f} per unit.\n"
        )
        """

    def sell_order(self, stock_price):
        units = self.orders[-1]["units"]
        return_sum = stock_price * units

        order = {
            "type": "SELL",
            "amount": return_sum,
            "price": stock_price,
            "units": units,
        }
        self.balance += return_sum
        profit = return_sum - self.orders[-1]["amount"]
        self.profit += profit

        """
        print(
            f"Sold ${return_sum:.2f} of {config["ticker"]} at ${stock_price:.2f} per unit."
        )
        print(
            f"Return: {((profit / self.orders[-1]["amount"]) * 100):.2f}% | Profit: ${profit:.2f}\n\nNew balance: ${self.balance}\n"
        )
        """

        self.orders.append(order)
