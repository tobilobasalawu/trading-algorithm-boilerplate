# Graph data class, has all graph data and can perform certain calculations on the data


class GraphData:
    def __init__(
        self,
        account,
        ticker,
        datetimes,
        closes,
        highs,
        lows,
        opens,
        ma_period,
        rsi_period,
        atr_period,
        std_dev_period,
        max_period,
        sma,
        rsi,
        atr,
        std_dev,
        entries,
        exits,
        ongoing_balance,
    ):
        self.account = account
        self.ticker = ticker
        self.datetimes = datetimes
        self.closes = closes
        self.highs = highs
        self.lows = lows
        self.opens = opens
        self.ma_period = ma_period
        self.rsi_period = rsi_period
        self.atr_period = atr_period
        self.std_dev_period = std_dev_period
        self.max_period = max_period
        self.sma = sma
        self.rsi = rsi
        self.atr = atr
        self.std_dev = std_dev
        self.entries = entries
        self.exits = exits
        self.ongoing_balance = ongoing_balance

    def calc_sma(self):
        self.sma = []
        closes = self.closes.to_list()
        for i in range(self.ma_period, len(closes)):
            window = closes[i - self.ma_period : i]
            self.sma.append(sum(window) / self.ma_period)
        return self.sma

    def calc_rsi(self):
        self.rsi = []
        closes = self.closes.to_list()
        for i in range(self.ma_period, len(closes)):
            no_gains = False
            no_losses = False
            window = closes[i - self.rsi_period : i]
            gains = []
            losses = []
            for j in range(len(window) - 1):
                if window[j + 1] - window[j] < 0:
                    losses.append(abs(window[j + 1] - window[j]))
                elif window[j + 1] - window[j] > 0:
                    gains.append(window[j + 1] - window[j])

            try:
                avg_gain = sum(gains) / len(gains)
            except ZeroDivisionError as error:
                no_gains = True
            try:
                avg_loss = sum(losses) / len(losses)
            except ZeroDivisionError as error:
                no_losses = True

            if no_gains == True:
                relative_strength = 0
            elif no_losses == True:
                relative_strength = 100
            else:
                relative_strength = avg_gain / avg_loss
            self.rsi.append(100 - (100 / (1 + relative_strength)))

        return self.rsi

    def calc_atr(self):
        self.atr = []

        highs = self.highs.to_list()
        lows = self.lows.to_list()
        closes = self.closes.to_list()

        true_ranges = []
        for i in range(1, len(closes)):
            high_low = highs[i] - lows[i]
            high_close = abs(highs[i] - closes[i - 1])
            low_close = abs(lows[i] - closes[i - 1])
            true_range = max(high_low, high_close, low_close)
            true_ranges.append(true_range)

        for i in range(self.atr_period, len(true_ranges) + 1):
            window = true_ranges[i - self.atr_period : i]
            self.atr.append(sum(window) / self.atr_period)

        return self.atr

    def calc_std_dev(self):
        self.std_dev = []
        closes = self.closes.to_list()

        for i in range(self.std_dev_period, len(closes) + 1):
            window = closes[i - self.std_dev_period : i]
            mean = sum(window) / self.std_dev_period
            variance = sum((x - mean) ** 2 for x in window) / self.std_dev_period
            std_dev = variance**0.5
            self.std_dev.append(std_dev)

        return self.std_dev
