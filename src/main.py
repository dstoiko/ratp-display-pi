#! /usr/bin/python3 -u
# -*- coding: utf-8 -*-

from os import path
import sys
import time
import traceback
import random

from trains import getAllStations, getDeparturesForStation
from utils import loadConfig
from display import Display


def loadData(station):
    print("Getting data for station: {} (line {})".format(
        station["name"], station["line"]))
    departures = getDeparturesForStation(station)
    print(departures)
    if len(departures) == 0 or (departures[0]["message"] in ["Service termine", "Schedules unavailable"]):
        return None

    return departures


def main(configPath):
    config = loadConfig(configPath)
    display = Display()
    stations = getAllStations() if (config["station"]["slug"] == "") else [
        config["station"]]

    timeLastUpdate = time.time() - config["refreshTime"]
    timeNow = time.time()
    while True:
        with display.regulator:
            if timeNow - timeLastUpdate >= config["refreshTime"]:
                if len(stations) == 1:
                    station = stations[0]
                else:
                    station = random.choice(stations)
                    station["direction"] = random.choice(["A", "R"])

                departures = loadData(station)
                if departures is None:
                    virtual = display.drawBlankSignage(station)
                else:
                    virtual = display.drawSignage(station, departures)

                timeLastUpdate = time.time()

            timeNow = time.time()
            virtual.refresh()


if __name__ == "__main__":
    try:
        configPath = path.abspath(
            path.join(path.dirname(__file__), "../config.json"))
        main(configPath)
    except KeyboardInterrupt:
        sys.exit(0)
    except ValueError as err:
        print(f"Error: {err}")
        traceback.print_exc()
        sys.exit(1)
    except KeyError as err:
        print(f"Error: Please ensure the {err} environment variable is set")
        traceback.print_exc()
        sys.exit(2)
