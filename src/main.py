#! /usr/bin/python3 -u
# -*- coding: utf-8 -*-

from os import path
import sys
import time
import traceback

from trains import loadDeparturesForStation
from utils import loadConfig
from display import Display


def loadData(journeyConfig):
    departures = loadDeparturesForStation(journeyConfig)

    if len(departures) == 0:
        return False, journeyConfig['departureStation']

    return departures, journeyConfig['departureStation']


def main(configPath):
    config = loadConfig(configPath)

    display = Display(config["color"])

    timeLastUpdate = time.time() - config["refreshTime"]
    timeNow = time.time()
    while True:
        with display.regulator:
            if timeNow - timeLastUpdate >= config["refreshTime"]:
                departures, departureStation = loadData(config["journey"])
                if departures == False:
                    virtual = display.drawBlankSignage(departureStation)
                else:
                    virtual = display.drawSignage(departures)

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
