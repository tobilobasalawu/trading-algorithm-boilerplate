class GraphData:
    def __init__(
        self,
        datetimes,
        closes,
        highs,
        lows,
        opens,
        ma_period,
        rsi_period,
        sma,
        rsi,
        entries,
        exits,
    ):
        self.datetimes = datetimes
        self.closes = closes
        self.highs = highs
        self.lows = lows
        self.opens = opens
        self.ma_period = ma_period
        self.rsi_period = rsi_period
        self.sma = sma
        self.rsi = rsi
        self.entries = entries
        self.exits = exits

    def calc_sma(self):
        self.sma = []
        closes = self.closes.to_list()
        for i in range(self.ma_period, len(closes) + 1):
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
