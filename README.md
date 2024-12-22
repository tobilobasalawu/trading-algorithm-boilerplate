# The Easiest Way to Create your Own Trading Algorithm!

Creating your own trading strategy has always been something you've wanted to explore, but you've always thought "it'll be way too hard" or "there will be so much learning I'll have to do beforehand", or maybe you're only really into the maths/finance aspect and don't want to bother with all the technical stuff?

It is now easier than ever to get stuck in to the maths and **create your own indicators** on a pre-setup Plotly graph. You won't need to worry about technical setup with this **stock trading algorithm bootstrapper**, which features various charting aspects, realtime indicators, simple implementation and a wide range of configurable settings.

You will be able to easily test your algorithm to see how it performs against both live and historical data. **This program only performs simulations, and does not trade with real money**.

_Please note: this project is a work-in-progress and may not yet come with a comprehensive list of visualisation features. This project is however open to pull requsts and you may contribute if you wish to do so._

## Getting started

You won't need any knowledge of UI development or various Python frameworks - this bootstrapper is designed for people who know (or want to learn) some Python, and want to put their coding and maths skills to the test. See the guide below for getting setup in under 5 minutes:

### Step 1

Make sure you have Python installed on your laptop. If you don't have it installed, you can install the latest version [here](https://www.python.org/downloads/).

### Step 2

Go to the top right of this repository and click 'fork'. This will add a copy of the repo into your profile.

### Step 3

Create a new folder on your laptop. Type into your terminal command line `cd path/to/your/new/folder` to change the working directory to your new folder. Then paste the following:

```shell
git clone https://github.com/your-username/trading-indicator.git
```

### Step 4

You now have a local copy of the forked repository in your new folder. In order to get it running, copy these 4 simple commands:

### **Windows**

Create a virtual environment to install your packages:

```shell
python -m venv .venv
```

Activate the virtual environment:

```shell
source .venv/Scripts/activate
```

Install your packages:

```shell
pip install -r requirements.txt
```

_If there are any ModuleNotFound errors after running this command, try installing the offending packages individually._

Run the server:

```shell
python main.py
```

---

### **MacOS/Linux**

Create a virtual environment to install your packages:

```shell
python3 -m venv .venv
```

Activate the virtual environment:

```shell
source .venv/bin/activate
```

Install your packages:

```shell
pip install -r requirements.txt
```

_If there are any ModuleNotFound errors after running this command, try installing the offending packages individually._

Run the server:

```shell
python3 main.py
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
account.buy_order(20) # 20 = closing price for a given candle
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
  "ticker": "GOOGL",
  "mostRecent": true,
  "interval": "5m",
  "startDate": "2024-12-01",
  "endDate": "2024-12-12",
  "timePeriod": "5d",
  "movingAvg": true,
  "maPeriod": 50,
  "rsiPeriod": 14,
  "addCsv": false,
  "initialBalance": 1000,
  "baseOrderValue": 100
}
```

_Most people using this tool won't need to worry about extra tools. For those wanting to add some extra customisation or their own features, see the docs below._

## Built-in functions:

### api/GraphData

Provides access to the `GraphData` class.

```python
rsi = my_data_object.calc_rsi()
# Calculate the RSI from the data in my_data_object

sma = my_data_object.calc_sma()
# Calculate the Simple Moving Average from the data in my_data_object
```

### api/fetch

- `get_df_selected_tf()`: Get the yfinance dataframe for a given timeframe.
- `get_df_recent()`: Get the most recent yfinance dataframe.
- `get_settings()`: Load the settings in `config.json` as a Python object.

### core/Account

Provides access to the `Account` class.

```python
my_account.buy_order(100, 20)
# Creates a buy order of $100 at $20 per share

my_account.sell_order(100)
# Create a sell order of $100

is_valid = my_account.check_balance()
# Checks if the starting balance is greater than the base order value (returns a boolean)
```

### core/order.py

See above for how to start adding indicators in this file.

### utils/convert.py

- `series_to_lists(data)`: Takes a Pandas dataframe as a parameter, and returns 5 datetime OHLC values as lists.

### utils/indicator.py

- `add(dict, key, value)`: Adds a key-value pair to a dictionary, and returns the new dictionary.
- `clear()`: Clears a dictionary.

## Future features

**Leverage**: Add leverage to a buy order.

**Accumulate short positions**: Open short positions.

**Comprehensive dashboard UI**: Check your trades in a dashboard.

**Create an account**: Keep track of all your past and present trades to see how your model performs over time.

## Contribute to this project

If you'd like to contribute to the project, follow these steps:

1. Fork this repository
2. Create a branch for your feature (`git checkout -b feature-name`)
3. Make changes and commit them (`git commit -am 'Add new feature'`)
4. Push to your forked repository (`git push origin feature-name`)
5. Submit a pull request

## Final notes

- Asset class focus: US equities
- Data source: yfinance

## Contact

If anything is unclear or you'd like to contact me, please create a new issue [here](https://github.com/JamieWells1/trading-indicator/issues/new).
