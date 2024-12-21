import yfinance as yf


# AAPL, "15m", "2024-12-11", "2024-12-18"
def get_df_selected_tf(
    ticker, _interval, _start_date, _end_date
):  # For a selected timeframe
    data = yf.download(ticker, interval=_interval, start=_start_date, end=_end_date)
    data["Ticker"] = ticker

    return data


# AAPL, "15m", "5d"
def get_df_recent(ticker, _interval, _period):  # For a selected timeframe
    data = yf.download(ticker, interval=_interval, period=_period)
    data["Ticker"] = ticker

    return data
