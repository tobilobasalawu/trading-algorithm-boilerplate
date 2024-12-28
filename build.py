import plotly.graph_objects as go
from plotly.subplots import make_subplots
import api.fetch as fetch
import core
import core.data
from core.Account import Account
from core.Backtest import Backtest
import utils.variables
import numpy as np


def build():
    config = fetch.get_settings()

    account = Account(
        uninvested_balance=config["initialBalance"],
        balance_absolute=config["initialBalance"],
        orders=[],
        profit=0,
        open_position_amount=0,
        total_invested=0,
        shares_owned=0,
        win_rate=0,
        completed_trades=0,
        profitable_trades=0,
    )

    data = core.data.init_graph_data(account)

    # Create a subplot layout with 2 rows
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        row_heights=[0.8, 0.2],
        subplot_titles=[f"{data.ticker} US Equity", "Average True Range (ATR)"],
    )

    # Add the candlestick chart
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

    fig.add_trace(candlestick, row=1, col=1)
    fig.add_trace(sma_line, row=1, col=1)

    # Add buy and sell markers to the candlestick chart
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
        ),
        row=1,
        col=1,
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
        ),
        row=1,
        col=1,
    )

    # Add the ATR line plot to the second row
    atr_line = go.Scatter(
        x=data.datetimes,
        y=data.atr,
        mode="lines",
        name="ATR",
        line=dict(color="#1f77b4", width=2),
    )
    fig.add_trace(atr_line, row=2, col=1)

    # Update layout
    fig.update_layout(
        title_text=f"{data.ticker} Analysis",
        xaxis=dict(gridcolor="#262626"),
        xaxis2=dict(
            title="Date", gridcolor="#262626"
        ),  # Second x-axis for the ATR chart
        yaxis=dict(title="Price ($)", gridcolor="#262626"),
        yaxis2=dict(title="ATR", gridcolor="#262626"),
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )

    return fig


def simulate():
    print("Working...\n")

    ongoing_balances = []

    chart_lines = []
    all_backtests = []
    config = fetch.get_settings()

    if config["simBestBacktests"] == False:
        iterations = config["simulations"]
    else:
        all_best_backtests = utils.variables.load_best_backtests()
        if len(all_best_backtests) > 0:
            iterations = len(all_best_backtests)
        else:
            print(
                "Cannot perform simulation on best backtests when there are none. Please restart the server."
            )
            quit()
    for i in range(iterations):

        account = Account(
            uninvested_balance=config["initialBalance"],
            balance_absolute=config["initialBalance"],
            orders=[],
            profit=0,
            open_position_amount=0,
            total_invested=0,
            shares_owned=0,
            win_rate=0,
            completed_trades=0,
            profitable_trades=0,
        )

        utils.variables.randomise()
        config = fetch.get_settings()

        if config["simBestBacktests"] == False:
            data = core.data.init_sim_data(account)
        else:
            try:
                data = core.data.init_backtest_data(all_best_backtests, account, i)
            except:
                print(
                    "Could not simulate existing backtest results. Has the file best backtests JSON file been populated?"
                )

        win_rate = (
            ((account.profitable_trades / account.completed_trades) * 100)
            if account.completed_trades > 0
            else -1
        )
        account.win_rate = win_rate

        # If new random backtests are being generated
        if config["simBestBacktests"] == True:
            backtest_result = Backtest(
                unique_id=utils.variables.generate_uid(6),
                ticker=all_best_backtests[i]["ticker"],
                sim_period=len(data.closes),
                total_investment=config["initialBalance"],
                final_amount=round(account.balance_absolute, 2),
                total_return=round(
                    (
                        (account.balance_absolute - config["initialBalance"])
                        / config["initialBalance"]
                        * 100
                    ),
                    2,
                ),
                win_rate=round(win_rate, 2),
                ma_period=all_best_backtests[i]["ma_period"],
                rsi_period=all_best_backtests[i]["rsi_period"],
                atr_period=all_best_backtests[i]["atr_period"],
                std_dev_period=all_best_backtests[i]["std_dev_period"],
                max_order_value=all_best_backtests[i]["max_order_value"],
                max_concurrent_positions=all_best_backtests[i][
                    "max_concurrent_positions"
                ],
                buy_multiplier=round(all_best_backtests[i]["buy_multiplier"], 2),
                band_multiplier=round(all_best_backtests[i]["band_multiplier"], 2),
            )

        # If existing backtests are being used
        else:
            backtest_result = Backtest(
                unique_id=utils.variables.generate_uid(6),
                ticker=config["ticker"],
                sim_period=len(data.closes),
                total_investment=config["initialBalance"],
                final_amount=round(account.balance_absolute, 2),
                total_return=round(
                    (
                        (account.balance_absolute - config["initialBalance"])
                        / config["initialBalance"]
                        * 100
                    ),
                    2,
                ),
                win_rate=round(win_rate, 2),
                ma_period=config["maPeriod"],
                rsi_period=config["rsiPeriod"],
                atr_period=config["atrPeriod"],
                std_dev_period=config["stdDevPeriod"],
                max_order_value=config["maxOrderValue"],
                max_concurrent_positions=config["maxConcurrentPositions"],
                buy_multiplier=round(config["buyMultiplier"], 2),
                band_multiplier=round(config["bandMultiplier"], 2),
            )

        line = go.Scatter(
            x=data.datetimes,
            y=data.ongoing_balance,
            mode="lines",
            name="Balance",
            line=dict(color=utils.variables.random_colour(), width=1),
            hovertemplate=f"Sim {backtest_result.unique_id}. Final balance: {backtest_result.final_amount}",
        )

        all_backtests.append(backtest_result)
        ongoing_balances.append(data.ongoing_balance)

        chart_lines.append(line)
        print(f"Finished simulation {(i + 1)}/{iterations}")

    max_ma_period = 0
    max_rsi_period = 0
    max_atr_period = 0
    max_std_dev_period = 0
    final_amounts = []
    total_returns = []

    for result in all_backtests:
        max_ma_period = max(max_ma_period, result.ma_period)
        max_rsi_period = max(max_rsi_period, result.rsi_period)
        max_atr_period = max(max_atr_period, result.atr_period)
        max_std_dev_period = max(max_std_dev_period, result.std_dev_period)
        final_amounts.append(result.final_amount)
        total_returns.append(result.total_return)

    final_amounts_percentile = np.percentile(
        final_amounts, config["topResultsPercentile"]
    )
    total_returns_percentile = np.percentile(
        total_returns, config["topResultsPercentile"]
    )

    top_backtests_count = 0
    new_best_backtests = []
    for result in all_backtests:
        if (
            result.final_amount > final_amounts_percentile
            or result.total_return > total_returns_percentile
        ) and config["simBestBacktests"] == False:
            utils.variables.add_to_top_results(result)
            top_backtests_count += 1
        elif (
            result.final_amount > final_amounts_percentile
            or result.total_return > total_returns_percentile
        ) and config["simBestBacktests"] == True:
            new_best_backtests.append(result)
            top_backtests_count += 1

    if config["simBestBacktests"] == True:
        utils.variables.overwrite_top_results(new_best_backtests)

    max_period_length = max(
        max_ma_period, max_rsi_period, max_atr_period, max_std_dev_period
    )
    shortest_line_length = len(data.closes) - max_period_length

    ongoing_balances = [balance[:shortest_line_length] for balance in ongoing_balances]

    for i in range(len(chart_lines)):
        chart_lines[i]["y"] = ongoing_balances[i]

    simulation_id = utils.variables.write_to_json(all_backtests)
    print(
        f"\nSimulation {simulation_id} complete. {top_backtests_count} backtests committed to best results.\n\n======================================================================"
    )

    fig = go.Figure(data=chart_lines)

    fig.update_layout(
        title=f"{data.ticker} US Equity",
        xaxis_title="Date",
        yaxis_title="Balance",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        xaxis=dict(
            type="category",
            tickmode="linear",
            dtick=(len(data.closes) / 10),
            gridcolor="#262626",
        ),
        yaxis=dict(gridcolor="#262626"),
        showlegend=False,
    )

    return fig
