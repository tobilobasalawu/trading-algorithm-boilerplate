# Trading Algorithm Boilerplate

This project provides a robust **trading algorithm simulator** that allows users to build, test, and optimize trading strategies using historical or live stock data. The platform features advanced candlestick visualizations, indicator plotting, and Monte Carlo simulations to find the best-performing parameter configurations. All tools are pre-configured, making it beginner-friendly yet powerful for advanced users.

---

## Features

- **Candlestick Charting**: Visualize stock prices alongside custom indicators.
- **Indicators**: Support for Moving Average (SMA), Relative Strength Index (RSI), Average True Range (ATR), and Standard Deviation.
- **Monte Carlo Simulations**: Run multiple simulations to optimize parameters.
- **Customizable Configurations**: Tweak settings in `config.json` to control backtesting parameters.
- **Real-Time and Historical Data**: Seamlessly switch between live and past data.

---

## Quickstart Guide

### 1. Install Python

Ensure Python (>= 3.7) is installed. Download it [here](https://www.python.org/downloads/).

### 2. Clone the Repository

Fork and clone this repository:

```shell
git clone https://github.com/your-username/trading-algorithm-boilerplate.git
cd trading-algorithm-boilerplate
```

### 3. Set up a Virtual Environment

### **On Windows:**

```shell
python -m venv .venv
source .venv/Scripts/activate
```

### **On Mac/Linux:**

```shell
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

```shell
pip install -r requirements.txt
```

### 5. Configure Settings

Open config.json and set your preferences:

- `ticker`: placeholder
- `simulate`: placeholder

Example:

```json
{
  "ticker": "AAPL",
  "simulate": true,
  "simulations": 50,
  "maPeriod": 20,
  "rsiPeriod": 14,
  "initialBalance": 10000
}
```

### 5. Run the Application:

Start the server:

```shell
python main.py
```

Visit [http://127.0.0.1:8050/](http://127.0.0.1:8050/) in your browser to see the charts.

---

## How it Works

1. Data Fetching: The app fetches stock data using the ticker and interval specified in `config.json`.
2. Indicator Calculations: SMA, RSI, and other metrics are computed for the dataset.
3. Simulations: Monte Carlo simulations iterate through possible parameter configurations to identify the best-performing strategies.
4. Visualization: Indicators and trade signals are plotted on an interactive candlestick chart using Plotly.

### Configurable Settings

- **Indicators**:
  - `maPeriod`: Period for SMA calculation.
  - `rsiPeriod`: Period for RSI calculation.
- **Simulations**:
  - `simulations`: Number of iterations to test.
  - `topResultsPercentile`: Filter top-performing simulations.
- **Backtesting**:
  - `initialBalance`: Starting balance for the account.
  - `baseOrderValue`: Minimum amount for trades.

---

## Creating your Algorithm

Modify `core/order.py` to define custom buy/sell logic. Use the pre-configured data such as:

- `account.rsi`: List of RSI values.
- `account.sma`: List of SMA values.
- `closes`: Closing prices.

Example:

```python
# Place a buy order
if account.rsi[i] < 30:
    entries = indicator.add(entries, datetimes[i], closes[i])
    account.buy_order(datetimes[i], baseOrderValue, closes[i])
    log.append("BUY")

# Place a sell order
elif account.rsi[i] > 70:
    exits = indicator.add(exits, datetimes[i], closes[i])
    account.sell_order(datetimes[i], closes[i])
    log.append("SELL")
```

---

## Visualisation

The platform dynamically updates visualizations, including:

- **Candlestick Charts**: Price movements.
- **Buy/Sell Markers**: Entry and exit points.
- **Indicator Lines**: SMA, RSI, and more.

You will simply need to save your Python files after changing them.

---

## Monte Carlo Simulations

To optimise strategies:

1. Set `simulate` to `true` in `config.json`.
2. Specify the number of simulations (`simulations`).
3. Initial results are saved for analysis, with top-performing strategies having the option to be re-simulated by setting `simBestBacktests` to `true`. The results from these simulations will overrwite the `results/.BEST-BACKTESTS.json` file with the new best backtest results.

---

## Roadmap

Future updates include:

- **Leverage**: Add leverage to a buy order.
- **Comprehensive** dashboard UI: Check your trades in a dashboard.
- **Simulations**: Measure how your algorithm performs when run through rigourous simulations.
- **Create an account**: Keep track of all your past and present trades to see how your model performs over time.

---

## Final notes:

- Asset class focus: US equities and ETFs
- Data source: yfinance

---

## Contribute

We welcome contributions! Submit pull requests or issues on [GitHub](https://github.com/JamieWells1/trading-algorithm-boilerplate/issues)
