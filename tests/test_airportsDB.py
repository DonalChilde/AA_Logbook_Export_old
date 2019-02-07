from airportsDB import airportsDB
import json
import logging
from dataclasses import asdict
from pathlib import Path

### setting up logger ####
logger = logging.getLogger(__name__)

#### Log Level ####
# NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
log_level = logging.DEBUG
# logLevel = logging.INFO
logger.setLevel(log_level)

#### Log Handler ####
log_formatter = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
# logger.addHandler(log_handler)


# def loadAirportsDB():
#     # dbPathString = "Python/resources/airportdb/airports.json"
#     dbPath = airportsDB.pathTo_MAIN_DB()
#     airportDB = airportsDB.load_Main_DB(dbPath)
#     return airportDB


def loadOpenFlightsCSV():
    filePath = airportsDB.pathTo_OpenFlightsCSV()
    data = airportsDB.load_OpenFLightsCSV(filePath)
    return data


def test_readOpenFlightsCSV():
    data = loadOpenFlightsCSV()
    print(len(data))
    print(data[:3])


def test_filterOpenFlights_iata():
    airports = loadOpenFlightsCSV()
    assert 5000 < len(airports) < 9000
    filtered = airportsDB.filter_Non_IATA_Airports(airports)
    assert 5000 < len(filtered) < 7000
    # print(len(filtered))
    # for airport in filtered:
    #     print(airport.name, airport.icao, airport.iata)


# def test_OpenFlights_Json():
#     savepath = airportsDB.pathToDataDirectory()/Path("openflights_airports.json")
#     data = loadOpenFlightsCSV()
#     dictList = [asdict(airport) for airport in data]
#     airportsDB.saveAirportJson(dictList, savepath)


def test_load_airports_IATA_json():
    data = airportsDB.load_airports_IATA_json()
    assert data["PHX"]


def test_load_airports_json():
    data = airportsDB.load_airports_json()
    assert 1000 < len(data) < 8000


def test_pathToDataDirectory():
    print(airportsDB.pathToDataDirectory())


# def test_filterOutNonIATAAirports():
#     airportDB = loadAirportsDB()
#     iataAirports = airportsDB.filterOutNon_IATA_Airports(airportDB)
#     # iataPath = airportsDB.pathTo_IATA_DB()
#     # airportsDB.saveAirportJson(iataAirports,iataPath)
#     assert iataAirports['PHX']


def test_loadandsaveairports():
    dbPath = Path("Python/resources/airportdb/iata_airports.json")
    airportDB = None
    with open(dbPath, "r") as inFile:
        airportDB = json.load(inFile)
        print(f"{len(airportDB)} in iata airport db")
    with open(dbPath, "w") as outFile:
        json.dump(airportDB, outFile, indent=2, sort_keys=True)
