from aaLogbook import airportsDB
import json
import logging
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
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s", datefmt='%d-%b-%y %H:%M:%S')
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
# logger.addHandler(log_handler)


def loadAirportsDB():
    dbPathString = "Python/resources/airportdb/airports.json"
    dbPath = Path(dbPathString)
    airportDB = airportsDB.loadMainDB(dbPath)
    return airportDB


def test_filterOutNonIATAAirports():
    airportDB = loadAirportsDB()
    iataAirports = airportsDB.filterOutNonIATAAirports(airportDB)
    airportsDB.saveAirportDB(
        Path("Python/resources/airportdb/iata_airports.json"), iataAirports)


def test_loadandsaveairports():
    dbPath = Path("Python/resources/airportdb/iata_airports.json")
    airportDB = None
    with open(dbPath, 'r') as inFile:
        airportDB = json.load(inFile)
        print(f"{len(airportDB)} in iata airport db")
    with open(dbPath, 'w') as outFile:
        json.dump(airportDB, outFile, indent=2, sort_keys=True)
