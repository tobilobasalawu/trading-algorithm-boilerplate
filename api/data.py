import yfinance as yf


# AAPL, "15m", "2024-12-11", "2024-12-18"
def get_df_selected_tf(
    ticker, _interval, _start_date, _end_date
):  # For a selected timeframe
    data = yf.download(ticker, interval=_interval, start=_start_date, end=_end_date)
    return data


# AAPL, "15m", "5d"
def get_df_recent(ticker, _interval, _period):  # For a selected timeframe
    data = yf.download(ticker, interval=_interval, period=_period)
    return data


class DataFrame:
    def __init__(self, df):
        self.df = df

    def get_ohlc(self, moving_avg):
        if moving_avg == True:
            closes = self.df.iloc[:, 1].values.tolist()
        else:
            closes = self.df.iloc[:, 1].iloc[20:].values.tolist()

        highs = self.df.iloc[:, 2].iloc[20:].values.tolist()
        lows = self.df.iloc[:, 3].iloc[20:].values.tolist()
        opens = self.df.iloc[:, 4].iloc[20:].values.tolist()
        return closes, highs, lows, opens
