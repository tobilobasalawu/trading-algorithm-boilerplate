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

## Setup result

You should now see something like this in your terminal:

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

Paste this URL into your browser and you should see a candlestick graph. Each time you update your code, this graph will automatically update.

## Creating your algorithm

The app is now all set up for you to start creating your algorithm in the `core/order.py` folder. You will see a section marked out for where to implement your logic, and don't worry - you won't need to install any other external packages from here on unless you wish to.

### How do I start adding indicators?

All indicators that are rendered on the graph are grabbed from the `entries` and `exits` dictionaries within the `order.py` file - this is where you'll be implementing your logic. They take a key (a datetime: string) and a value (close price: integer) - this is the closing price for any given candle.

```python
# Format => datetime (string): close price (integer)
entries = {
    "2024-12-01": 100
    "2024-12-03": 80
}

exits = {
    "2024-12-02": 120
    "2024-12-04": 110
}
```

In order to add **entries**, you will need to use these 3 lines of code:

```python
entries = indicator.add(entries, "2024-12-01", 20) # "2024-12-01" = your datetime, 20 = closing price for a given candle
account.buy_order(100, 20) # 100 = base order value, 20 = closing price for a given candle
log.append("BUY")
```

In order to add **exits**, you will need to use these 3 lines of code:

```python
exits = indicator.add(exits, "2024-12-01", 20) # "2024-12-01" = your datetime, 20 = closing price for a given candle
account.sell_order(20) # 20 = closing price for a given candle
log.append("SELL")
```

To help your algorithm decide when to create an indicator, you have the following data available **for all rendered candles**:

- `datetimes`: A list of all datetimes.
- `opens`: A list of opening prices.
- `closes`: A list of closing prices.
- `highs`: A list of high prices.
- `lows`: A list of low prices.
- `account.rsi`: A list of RSI values.
- `account.sma`: A list of SMA values.

All these values line up for each of your candles. For example, if you took:

```python
datetimes[6]
opens[6]
account.rsi[6]
```

Each value would correlate to the same candle; the 7th candle.

If you shut your app down and decide you want to re-run it, you won't have to create a new virtual environment, you'll just have to re-activate your existing one in a new terminal.

## Testing your algorithm

If you've made some changes and you'd like to see them in action, you can either wait for the web page to update (it updates every time you save your code), or you can reactivate your virtual environment by following the setup steps above and running `python main.py` if you're using Windows or `python3 main.py` if you're using MacOS/Linux.

## Docs

All the configurable settings can be found in [config.json](https://github.com/JamieWells1/trading-indicator/blob/main/config.json). Have a play around with this and decide what settings you want for your trading strategy.

## config.json

- `ticker`: Change the stock being loaded
- `mostRecent`: Set whether the chart uses the most recent data for the loaded stock
- `interval`: Specifies the time interval between each candle in the chart
- `startDate`: Set when the chart should load data from (only applies if `mostRecent` is set to false)
- `endDate`: Set when the chart should load data up to (only applies if `mostRecent` is set to false)
- `timePeriod`: Specifies the time period used for analyzing data (only applies if `mostRecent` is set to true)
- `movingAvg`: Specifies whether to calculate and display a **Moving Average** (MA) on the chart
- `maPeriod`: Defines the period (number of candles) used to calculate the Moving Average
- `rsiPeriod`: Defines the period (number of candles) used to calculate the **Relative Strength Index** (RSI)
- `addCsv`: Determines whether or not to export the chart's data to a CSV file (available at root folder directory)
- `initialBalance`: Specifies the initial balance of the trading account
- `baseOrderValue`: Defines the base amount used for each trade order

Example JSON configuration:

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
  "bandMultiplier": 1.5,
  "stoplossAtrMultiplier": 1.5,
  "takeprofitAtrMultiplier": 2.5,
  "renderStoplossTakeprofit": true
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
