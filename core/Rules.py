import api.fetch as api


class Rules:
    def __init__(self, payload):
        self.payload = payload
        self.config = api.get_settings()

    def balance_valid(self):
        initial_buy_amount = self.payload["initial_buy_amount"]
        if initial_buy_amount > self.config["maxOrderValue"]:
            initial_buy_amount = self.config["maxOrderValue"]
        if initial_buy_amount > self.payload["uninvested_balance"]:
            initial_buy_amount = self.payload["uninvested_balance"]

        if initial_buy_amount > 0:
            response = {"valid": True, "amount": initial_buy_amount}
        else:
            response = {"valid": False, "amount": 0}

        return response

    # Go through all the rules
    def correctify(self):
        pass
