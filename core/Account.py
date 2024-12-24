import utils.indicator as indicator
import api.fetch as api

config = api.get_settings()


class Account:
    def __init__(self, balance, orders, profit, open_position_amount, total_invested):
        self.balance = balance  # Initial balance
        # e.g. 10 = minimum of 10% of account balance put into each trade
        self.orders = (
            orders  # List of dicts: order amount, buy/sell price, units bought
        )
        self.profit = profit
        self.open_position_amount = open_position_amount
        self.total_invested = total_invested

    def buy_order(self, order_value, stock_price):  # Place a buy order
        order = {
            "type": "BUY",
            "amount": order_value,
            "price": stock_price,
        }

        self.balance -= order["amount"]
        self.total_invested += order["amount"]
        try:
            self.open_position_amount = (
                self.open_position_amount * (stock_price / self.orders[-1]["price"])
            ) + order["amount"]
        except:
            self.open_position_amount += order["amount"]

        self.orders.append(order)

    def sell_order(self, stock_price):  # Place a sell order
        return_sum = self.open_position_amount * (
            stock_price / self.orders[-1]["price"]
        )

        order = {
            "type": "SELL",
            "amount": return_sum,
            "price": stock_price,
        }

        self.balance += return_sum
        self.profit += return_sum - self.total_invested
        self.total_invested = 0
        self.open_position_amount = 0

        self.orders.append(order)

        """
        print(
            f"Sold ${return_sum:.2f} of {config["ticker"]} at ${stock_price:.2f} per unit."
        )
        print(
            f"Return: {((profit / self.orders[-1]["amount"]) * 100):.2f}% | Profit: ${profit:.2f}\n\nNew balance: ${self.balance}\n"
        )
        """

    def check_balance(self):  # Does an initial balance check
        if config["initialBalance"] < config["baseOrderValue"]:
            return False
        else:
            return True
