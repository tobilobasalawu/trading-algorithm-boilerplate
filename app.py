# Price action mean reversion backtesting
import sys, os, json

from dash import Dash, html, dcc, Input, Output

import build as graph
import api.fetch as api
from core.Account import Account

app = Dash(
    __name__,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootswatch@5.1.3/dist/cyborg/bootstrap.min.css"
    ],
)

# App layout
app.layout = html.Div(
    [
        dcc.Graph(id="candles", style={"height": "100vh"}),
        dcc.Interval(id="interval", interval=200000),
    ]
)


@app.callback(
    Output("candles", "figure"),
    Input("interval", "n_intervals"),
)
def update_graph(n_intervals):
    config = api.get_settings()

    if config["mostRecent"] == False:
        df, ticker = api.get_df_selected_tf(
            config["ticker"], config["interval"], config["startDate"], config["endDate"]
        )
    else:
        df, ticker = api.get_df_recent(
            config["ticker"], config["interval"], config["timePeriod"]
        )
    df = df.iloc[:-1]

    account = Account(config["initialBalance"], config["baseOrderValue"], [], 0, 0)

    try:
        return graph.build(
            account,
            df,
            ticker,
            moving_avg=config["movingAvg"],
            ma_period=config["maPeriod"],
            rsi_period=config["rsiPeriod"],
            add_csv=config["addCsv"],
        )
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"\nGraph failed to load: {e} => {fname, exc_tb.tb_lineno}\n")
    if not Exception:

        print("\n<========== Graph updated successfully ==========>\n")


def main():
    app.run_server(debug=True)
