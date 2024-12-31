# Variables for running simulations

import random, json, string, os
import api.fetch as api


def randomise():
    config = api.get_settings()
    # config["maPeriod"] = random.randint(160, 240)
    config["rsiPeriod"] = random.randint(10, 20)
    config["atrPeriod"] = random.randint(15, 25)
    config["stdDevPeriod"] = random.randint(15, 30)
    config["maxOrderValue"] = random.randint(
        (int(0.2 * config["initialBalance"])), (int(0.8 * config["initialBalance"]))
    )
    config["maxConcurrentPositions"] = random.randint(2, 10)
    config["buyMultiplier"] = random.uniform(1, 3)
    config["bandMultiplier"] = random.uniform(1, 2)
    config["advanced"]["stoplossAtrPeriod"] = random.randint(
        15, 25
    )  # The ATR period used for determining stoploss
    config["advanced"]["stoplossAtrMultiplier"] = random.uniform(
        1.5, 2.5
    )  # The ATR multiplier used for determining stoploss
    config["advanced"]["previousXBarsStrategy"] = random.randint(
        4, 8
    )  # How many bars to go back to determine buy and sell signals for strategies which use previous candles
    config["advanced"]["lowLowHighHighStrategy"] = random.randint(
        4, 8
    )  # How many bars to go back to determine buy and sell signals for lowest low highest high strategy
    config["advanced"]["constantOfStandardisation"] = random.randint(
        2, 100
    )  # Constant used to standardise the output values of various strategies
    config["advanced"]["zValueTriggerTheshold"] = random.uniform(0.8, 1.6)
    config["advanced"]["breakoutPeriod"] = random.randint(45, 75)

    with open("config.json", "w") as settings:
        json.dump(config, settings, indent=2)


def generate_uid(length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))


def write_to_json(all_backtests):
    simulation_id = generate_uid(6)
    file_path = os.path.join("z.results", f"sim-{simulation_id}.json")
    all_backtest_dicts = [backtest.to_dict() for backtest in all_backtests]

    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)

    return simulation_id


def add_to_top_results(result):
    file_path = os.path.join("z.results", ".BEST-BACKTESTS.json")

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print(
            f"Warning: {file_path} is empty or contains invalid JSON. Initializing empty list."
        )
        existing_data = []

    existing_data.append(result.to_dict())

    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=2)


def load_best_backtests():
    file_path = os.path.join("z.results", f".BEST-BACKTESTS.json")

    try:
        with open(file_path, "r") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(
            f"Warning: {file_path} is empty, missing, or invalid. Returning an empty list."
        )
        existing_data = []

    return existing_data


def overwrite_top_results(backtests_to_write):
    file_path = os.path.join("z.results", f".BEST-BACKTESTS.json")

    all_backtest_dicts = [backtest.to_dict() for backtest in backtests_to_write]
    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)


def random_colour():
    letters = "0123456789ABCDEF"
    color = "#"
    for i in range(6):
        color += letters[random.randint(0, 15)]
    return color


def generate_number(digits):
    number = ""
    for i in range(digits):
        digit = str(random.randint(0, 9))
        number += digit
    return number
