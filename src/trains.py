import os
import requests
import json


def loadDeparturesForStation(journeyConfig):
    departureStation = journeyConfig["departureStationSlug"]
    line = journeyConfig["line"]
    direction = journeyConfig["direction"]
    URL = f"https://api-ratp.pierre-grimaud.fr/v4/schedules/metros/{line}/{departureStation}/{direction}"
    r = requests.get(url=URL)
    data = r.json()
    return data["result"]["schedules"]


if __name__ == "__main__":
    with open('config.json', 'r') as jsonConfig:
        config = json.load(jsonConfig)
    print('Config loaded:')
    print(config)
    departures = loadDeparturesForStation(config["journey"])
    print(departures)
