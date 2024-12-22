import plotly.graph_objects as go
import api.GraphData as api
import api.fetch as fetch
import core.order as order

config = fetch.get_settings()


def init_data(account, df, moving_avg=True, ma_period=20, rsi_period=14):
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
        account,
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

    data_obj.entries, data_obj.exits = order.indicators(account, data_obj, rsi)

    if account.profit > 0:
        profit_colour = "\033[32m"
    elif account.profit < 0:
        profit_colour = "\033[31m"
    reset_colour = "\033[0m"

    print(
        "\n=====================================================================================\n"
    )
    print(
        f"Made {len(account.orders) // 2} trades | Volume traded: ${account.volume:.2f} | {profit_colour}Return: {((account.profit / config["initialBalance"]) * 100):.2f}%{reset_colour} | {profit_colour}Profit: ${account.profit:.2f}{reset_colour}\n"
    )

    return data_obj


def build(
    account, df, ticker, moving_avg=True, ma_period=20, rsi_period=14, add_csv=True
):

    if add_csv == True:
        df.to_csv("data.csv")
    data = init_data(account, df, moving_avg, ma_period, rsi_period)

    candlestick = go.Candlestick(
        x=data.datetimes,
        open=data.opens,
        high=data.highs,
        low=data.lows,
        close=data.closes,
        name="Price ($)",
        increasing=dict(line=dict(color="#199e5c")),
        decreasing=dict(line=dict(color="#eb4034")),
        increasing_fillcolor="#199e5c",
        decreasing_fillcolor="#eb4034",
    )

    sma_line = go.Scatter(
        x=data.datetimes,
        y=data.sma,
        mode="lines",
        name="SMA",
        line=dict(color="orange", width=1),
    )

    fig = go.Figure(data=[candlestick, sma_line])

    fig.add_trace(
        go.Scatter(
            x=data.entries.index,
            y=data.entries,
            mode="markers",
            name="BUY",
            marker_symbol="arrow-up",
            marker_size=15,
            marker_line_width=2,
            marker_line_color="#eee",
            marker_color="#0ac91d",
            hovertemplate="BUY: %{y}",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data.exits.index,
            y=data.exits,
            mode="markers",
            name="SELL",
            marker_symbol="arrow-down",
            marker_size=15,
            marker_line_width=2,
            marker_line_color="#eee",
            marker_color="#b0160e",
            hovertemplate="SELL: %{y}",
        )
    )

    fig.update_layout(
        title=f"{ticker} US Equity",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        xaxis=dict(type="category", tickmode="linear", dtick=ma_period),
    )

    return fig
