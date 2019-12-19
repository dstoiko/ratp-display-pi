import os
import sys
import time
import json
import traceback

from trains import loadDeparturesForStation
from utils import loadConfig, makeFonts
from display import Display

from luma.core.interface.serial import spi
from luma.oled.device import ssd1322
from luma.core.sprite_system import framerate_regulator


def loadData(journeyConfig):
    departures = loadDeparturesForStation(journeyConfig)

    if len(departures) == 0:
        return False, journeyConfig['departureStation']

    return departures, journeyConfig['departureStation']


def main():
    config = loadConfig()
    serial = spi()
    device = ssd1322(serial, mode="1", rotate=2)
    fonts = makeFonts()

    widgetWidth = 256
    widgetHeight = 64

    regulator = framerate_regulator(fps=10)
    display = Display(fonts, config["color"])

    timeLastUpdate = time.time() - config["refreshTime"]
    timeNow = time.time()
    while True:
        with regulator:
            if timeNow - timeLastUpdate >= config["refreshTime"]:
                departures, departureStation = loadData(config["journey"])
                if departures == False:
                    virtual = display.drawBlankSignage(
                        device, widgetWidth, widgetHeight, departureStation)
                else:
                    virtual = display.drawSignage(
                        device, widgetWidth, widgetHeight, departures)

                timeLastUpdate = time.time()

            timeNow = time.time()
            virtual.refresh()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except ValueError as err:
        print(f"Error: {err}")
        traceback.print_exc()
    except KeyError as err:
        print(f"Error: Please ensure the {err} environment variable is set")
        traceback.print_exc()
