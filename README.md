# The Easiest Way to Create your Own Trading Algorithm!

Creating your own trading strategy has always been something you've wanted to explore, but you've always thought "it'll be way too hard" or "there will be so much learning I'll have to do beforehand", or maybe you're only really into the maths/finance aspect?

It is now easier than ever to get stuck in to the maths and **create your own indicators** on a pre-setup Plotly graph. You won't need to worry about technical setup with this **stock trading algorithm bootstrapper**, featuring various charting aspects, realtime indicators, simple implementation and a wide range of configurable settings.

_Please note: this project is a work-in-progress and may not yet come with a comprehensive list of visualisation features. This project is however open to pull requsts and you may contribute your own if you wish to do so._

## Getting started

You won't need any knowledge of UI or various Python frameworks - this bootstrapper is designed for people who know (or want to learn) some Python, and want to put their coding and maths skills to the test. See the guide below for getting setup in under 5 minutes:

### Step 1

Make sure you have Python installed on your laptop. If you don't have it installed, you can install the latest version [https://www.python.org/downloads/](here)

### Step 2

Go to the top right of this repository and click 'fork'. This will add a copy of the repo into your profile.

### Step 3

Create a new folder on your laptop. Type into your command line `cd path/to/your/new/folder` to change the working directory to your new folder. Then paste the following:

```shell
git clone https://github.com/your-username/trading-indicator.git
```

### Step 4

You now have a local copy of the forked repository in your new folder. In order to get it running, copy these 4 simple commands:

**Windows**

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

Run the server:

```shell
python main.py
```

---

**MacOS/Linux**

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

Run the server:

```shell
python3 main.py
```

Now you should see something like this in your terminal:

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app 'app'
 * Debug mode: on
```

Paste this URL into your browser and you should see a candlestick graph. Each time you update your code, this graph will automatically update.

## Docs

All the configurable settings can be found in [https://github.com/JamieWells1/trading-indicator/blob/main/config.json](config.json). Have a play around with this and decide what settings you want for your trading strategy.

## Future features

## Notes

- Asset class focus: US equities
- Data source: yfinance
