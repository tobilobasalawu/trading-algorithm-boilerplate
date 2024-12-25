# Variables for running simulations

import random, json, string, os
import api.fetch as api


def randomise():
    config = api.get_settings()
    config["maPeriod"] = random.randint(14, 50)
    config["rsiPeriod"] = random.randint(7, 20)
    config["atrPeriod"] = random.randint(7, 20)
    config["stdDevPeriod"] = random.randint(7, 20)
    config["maxOrderValue"] = random.randint(
        (int(0.2 * config["initialBalance"])), (int(0.8 * config["initialBalance"]))
    )
    config["maxConcurrentPositions"] = random.randint(2, 10)
    config["buyMultiplier"] = random.uniform(1, 3)
    config["bandMultiplier"] = random.uniform(1, 2)

    with open("config.json", "w") as settings:
        json.dump(config, settings, indent=2)


def generate_uid(length):
    letters = string.ascii_lowercase + string.ascii_uppercase
    return "".join(random.choice(letters) for i in range(length))


def write_to_json(all_backtests):
    simulation_id = generate_uid(6)
    file_path = os.path.join("results", f"sim-{simulation_id}.json")
    all_backtest_dicts = [backtest.to_dict() for backtest in all_backtests]

    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)

    return simulation_id


def add_to_top_results(result):
    file_path = os.path.join("results", ".BEST-BACKTESTS.json")

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
    file_path = os.path.join("results", f".BEST-BACKTESTS.json")

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
    file_path = os.path.join("results", f".BEST-BACKTESTS.json")

    all_backtest_dicts = [backtest.to_dict() for backtest in backtests_to_write]
    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)


def random_colour():
    letters = "0123456789ABCDEF"
    color = "#"
    for i in range(6):
        color += letters[random.randint(0, 15)]
    return color
