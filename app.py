# Price action mean reversion backtesting
import statistics

from dash import Dash, html, dcc, Output, Input
import pandas as pd
import numpy as np

import api.data as api
import utils.calcs as calcs
import utils.build as graph

app = Dash()


app.layout = html.Div(
    [
        dcc.Graph(id="candles"),
        dcc.Interval(id="interval", interval=200000),
    ]
)


def init(moving_avg=True, ma_period=20):
    df = api.get_df_selected_tf("TSLA", "15m", "2024-12-11", "2024-12-18").iloc[
        :-1
    ]  # exclude last row (in case it's a live candle)
    df_object = api.DataFrame(df)
    closes, highs, lows, opens = df_object.get_ohlc(moving_avg)

    if moving_avg == True:
        sma = calcs.calc_sma(
            closes, ma_period
        )  # List of closing values, moving-average period length
        closes = closes[ma_period:]  # Remove excess closing values

    print(df)
    graph.build(df)


def main():
    app.run_server(debug=True)
    init()
