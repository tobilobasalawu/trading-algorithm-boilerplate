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

Open config.json and set your preferences. For example:

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

There are some more advanced settings that you can set if you wish for further customisation.

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

Below is a comprehensive list of all configurable settings available in `config.json`:

- **General**:

  - `ticker`: The stock ticker to load data for (e.g., `"AAPL"` for Apple).
  - `simulate`: Boolean (`true`/`false`) to enable or disable simulations.
  - `mostRecent`: Boolean (`true`/`false`) to specify whether the app uses the most recent data or a custom date range.
  - `interval`: Time interval between each candle (e.g., `"1d"`, `"60m"`, `"5m"`).
  - `timePeriod`: Specifies the time period for analysis when `mostRecent` is `true` (e.g., `"5d"`).
  - `startDate`: Start date for data when `mostRecent` is `false` (format: `"YYYY-MM-DD"`).
  - `endDate`: End date for data when `mostRecent` is `false` (format: `"YYYY-MM-DD"`).
  - `addCsv`: Boolean (`true`/`false`) to determine whether the candlestick chart data should be exported to a CSV file.

- **Indicators**:

  - `maPeriod`: Number of candles used to calculate the Simple Moving Average (SMA).
  - `rsiPeriod`: Number of candles used to calculate the Relative Strength Index (RSI).
  - `atrPeriod`: Number of candles used to calculate the Average True Range (ATR).
  - `stdDevPeriod`: Number of candles used to calculate the Standard Deviation.

- **Simulations**:
  - `simulations`: Number of Monte Carlo simulations to run for parameter optimization.
  - `simBestBacktests`: Boolean (`true`/`false`) to enable or disable using the best backtest results for further simulations.
  - `topResultsPercentile`: Percentile of top-performing simulations to save (e.g., `90` for top 10%).
- **Backtesting**:
  - `initialBalance`: Starting balance of the trading account.
  - `baseOrderValue`: Minimum amount allocated for a single trade.
  - `maxOrderValue`: Maximum allowable value for a single trade.
  - `maxConcurrentPositions`: Maximum number of open positions allowed simultaneously.
  - `buyMultiplier`: Multiplier applied to entry capital for calculating trade size.
  - `bandMultiplier`: Number of standard deviations used for mean reversion triggers.

### Example `config.json`

```json
{
  "ticker": "MSFT",
  "simulate": false,
  "simulations": 10,
  "simBestBacktests": false,
  "topResultsPercentile": 90,
  "mostRecent": true,
  "interval": "1d",
  "timePeriod": "1y",
  "startDate": "2020-12-01",
  "endDate": "2024-12-01",
  "maPeriod": 50,
  "rsiPeriod": 7,
  "atrPeriod": 20,
  "stdDevPeriod": 20,
  "addCsv": true,
  "initialBalance": 10000,
  "baseOrderValue": 1000,
  "maxOrderValue": 5000,
  "maxConcurrentPositions": 4,
  "buyMultiplier": 1.2,
  "bandMultiplier": 1.5
}
```

---

## Creating your Algorithm

In order to create a **buy** signal, you will need to use these 3 lines of code:

```python
buy(entries, <amount>, <price>)

# Example:

buy(entries, config["baseOrderValue"], candles[i]["close"])
# Place a buy order for the base order amount defined in config.json, buy at the closing price of the current candle
```

In order to create a **sell** signal, you will need to use these 3 lines of code:

```python
sell(exits, <price>)

# Example:

sell(exits, candles[i]["close"])
# Place a sell order at the closing price of the current candle
```
To help your algorithm decide when to create an indicator, you have the following data available **for each rendered candle**:
```python
candle["datetime"]  # Datetime of the candle
candle["open"]  # Open price of the candle
candle["close"]  # Close price of the candle
candle["high"]  # High price of the candle
candle["low"]  # Low price of the candle
candle["sma"]  # Moving average at the candle
candle["rsi"]  # Relative strength index at the candle
candle["atr"]  # Average true range at the candle
candle["std_dev"]  # Standard deviation at the candle
```
You will be able to access these candles by iterating through each entry in the 'candles' list in `order.py`.

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
3. Initial results are saved for analysis, with top-performing strategies having the option to be re-simulated by setting `simBestBacktests` to `true`. The results from these simulations will overrwite the `z.results/.BEST-BACKTESTS.json` file with the new best backtest results.

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
