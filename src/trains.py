import os
import requests
import json


BASE_URL = "https://api-ratp.pierre-grimaud.fr/v4"


def getAllStations():
    stations = []
    linesUrl = f"{BASE_URL}/lines/metros"
    r = requests.get(linesUrl)
    data = r.json()

    for line in data["result"]["metros"]:
        line = line["code"]
        stationsUrl = f"{BASE_URL}/stations/metros/{line}"
        r = requests.get(stationsUrl)
        data = r.json()
        lineStations = data["result"]["stations"]
        # Add line number, we will need it later on
        for s in lineStations:
            s["line"] = line
        stations.extend(lineStations)

    return stations


def getDeparturesForStation(station):
    line = station["line"]
    slug = station["slug"]
    direction = station["direction"]
    url = f"{BASE_URL}/schedules/metros/{line}/{slug}/{direction}"
    r = requests.get(url)
    data = r.json()
    return data["result"]["schedules"]


if __name__ == "__main__":
    with open('config.json', 'r') as jsonConfig:
        config = json.load(jsonConfig)
    print('Config loaded:')
    print(config)
    departures = getDeparturesForStation(config["journey"])
    print(departures)
