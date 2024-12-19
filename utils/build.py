from dash import Dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd


def build(df):
    print(df)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["Datetime"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )

    fig.update_layout(
        title="Basic Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    fig.show()
