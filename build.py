import plotly.graph_objects as go
import api.GraphData as api
import api.fetch as fetch
import core.order as order
from core.Account import Account

config = fetch.get_settings()


def init_data():
    if config["mostRecent"] == False:
        df, ticker = fetch.get_df_selected_tf(
            config["ticker"], config["interval"], config["startDate"], config["endDate"]
        )
    else:
        df, ticker = fetch.get_df_recent(
            config["ticker"], config["interval"], config["timePeriod"]
        )
    df = df.iloc[:-1]

    ma_period = config["maPeriod"]
    rsi_period = config["rsiPeriod"]

    datetimes = df.index.to_series()[ma_period:]
    closes = df.iloc[:, 0]
    highs = df.iloc[ma_period:, 1]
    lows = df.iloc[ma_period:, 2]
    opens = df.iloc[ma_period:, 3]
    rsi = []
    sma = []
    entries = []
    exits = []

    account = Account(config["initialBalance"], [], 0, 0, 0)
    # Create account object that will be used for your session

    valid = account.check_balance()
    if valid == False:
        print(
            "\nError: Base order value cannot be greater than starting amount. Please restart the server.\n"
        )
        quit()

    if config["addCsv"] == True:
        df.to_csv("data.csv")

    data_obj = api.GraphData(
        account,
        ticker,
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

    if config["movingAvg"]:
        data_obj.sma = (
            data_obj.calc_sma()
        )  # List of closing values, moving-average period length
        data_obj.closes = data_obj.closes.iloc[
            ma_period:
        ]  # Remove excess closing values
    else:
        data_obj.closes = data_obj.closes.iloc[ma_period:, 1]

    data_obj.entries, data_obj.exits = order.indicators(account, data_obj)

    profit_colour = "\033[0m"
    if account.profit > 0:
        profit_colour = "\033[32m"
    elif account.profit < 0:
        profit_colour = "\033[31m"
    reset_colour = "\033[0m"

    print(
        "\n=====================================================================================\n"
    )
    print(
        f"Made {len(account.orders) // 2} trades | {profit_colour}Return: {((account.profit / config['initialBalance']) * 100):.2f}%{reset_colour} | {profit_colour}Profit: ${account.profit:.2f}{reset_colour}\n"
    )

    return data_obj


def build():
    data = init_data()

    candlestick = go.Candlestick(
        x=data.datetimes,
        open=data.opens,
        high=data.highs,
        low=data.lows,
        close=data.closes,
        name="Price ($)",
        increasing=dict(line=dict(color="#16a16e")),
        decreasing=dict(line=dict(color="#eb4034")),
        increasing_fillcolor="#16a16e",
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
        title=f"{data.ticker} US Equity",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        xaxis=dict(type="category", tickmode="linear", dtick=config["maPeriod"]),
    )

    return fig
