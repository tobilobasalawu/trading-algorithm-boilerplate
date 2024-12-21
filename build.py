import plotly.graph_objects as go
import api.GraphData as api
import utils.calcs as calcs
import pandas as pd


def init_data(df, moving_avg=True, ma_period=20, rsi_period=14):
    print(df.head())
    datetimes = df.index.to_series()[ma_period:]
    closes = df.iloc[:, 0]
    highs = df.iloc[ma_period:, 1]
    lows = df.iloc[ma_period:, 2]
    opens = df.iloc[ma_period:, 3]
    rsi = []
    sma = []
    entries = []
    exits = []

    data_obj = api.GraphData(
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
    )

    rsi = data_obj.calc_rsi()

    if moving_avg == True:
        data_obj.sma = (
            data_obj.calc_sma()
        )  # List of closing values, moving-average period length
        data_obj.closes = data_obj.closes.iloc[
            ma_period:
        ]  # Remove excess closing values
    else:
        data_obj.closes = data_obj.closes.iloc[ma_period:, 1]

    data_obj.entries, data_obj.exits = calcs.indicators(data_obj, rsi)

    return data_obj


def build(df, moving_avg=True, ma_period=20, rsi_period=14, add_csv=True):

    if add_csv == True:
        df.to_csv("data.csv")
    data = init_data(df, moving_avg, ma_period, rsi_period)

    candlestick = go.Candlestick(
        x=data.datetimes,
        open=data.opens,
        high=data.highs,
        low=data.lows,
        close=data.closes,
        increasing=dict(line=dict(color="#199e5c")),
        decreasing=dict(line=dict(color="#eb4034")),
        increasing_fillcolor="#199e5c",
        decreasing_fillcolor="#eb4034",
    )

    sma_line = go.Scatter(
        x=data.datetimes,  # Ensure this matches the candlestick's x-axis
        y=data.sma,  # The moving average values
        mode="lines",  # Line chart
        name="SMA",  # Legend label for the moving average
        line=dict(color="white", width=1),  # Customize the line style
    )

    fig = go.Figure(data=[candlestick, sma_line])

    fig.add_trace(
        go.Scatter(
            x=data.entries.index,
            y=data.entries,
            mode="markers",
            marker_symbol="diamond-dot",
            marker_size=10,
            marker_line_width=1,
            marker_line_color="#262626",
            marker_color="#0ac91d",
            hovertemplate="BUY: %{y}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.exits.index,
            y=data.exits,
            mode="markers",
            marker_symbol="diamond-dot",
            marker_size=10,
            marker_line_width=1,
            marker_line_color="#262626",
            marker_color="#b0160e",
            hovertemplate="SELL: %{y}",
        )
    )

    fig.update_layout(
        title="Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        xaxis=dict(type="category", tickmode="linear", dtick=ma_period),
    )

    return fig
