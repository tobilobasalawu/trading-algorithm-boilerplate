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
    file_path = os.path.join("results", f"sim-{generate_uid(6)}.json")
    all_backtest_dicts = [backtest.to_dict() for backtest in all_backtests]

    with open(file_path, "w") as file:
        json.dump(all_backtest_dicts, file, indent=2)


def random_colour():
    letters = "0123456789ABCDEF"
    color = "#"
    for i in range(6):
        color += letters[random.randint(0, 15)]
    return color
