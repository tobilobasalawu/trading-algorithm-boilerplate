# Price action mean reversion backtesting
import sys, os

from dash import Dash, html, dcc, Input, Output

import build as graph
import api.fetch as api

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
    df = api.get_df_selected_tf("JMIA", "15m", "2024-12-01", "2024-12-20").iloc[:-1]

    try:
        return graph.build(
            df, moving_avg=True, ma_period=50, rsi_period=14, add_csv=True
        )
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"\nGraph failed to load: {e} => {fname, exc_tb.tb_lineno}\n")
    if not Exception:

        print("\n<========== Graph updated successfully ==========>\n")


def main():
    app.run_server(debug=True)
