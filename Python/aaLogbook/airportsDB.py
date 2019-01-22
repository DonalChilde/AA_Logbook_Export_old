"""
will provide interface for airport lookup.
load db to in memory sqlite? or just lookup from json.
simplest solution first, then play and do speed testing.
"""
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

class AirportsDB():

    def __init__(self,pathToMainDB, pathToIATADB):
        self.pathToMainDB = pathToMainDB
        self.pathToIATADB = pathToIATADB
        

def loadMainDB(pathToMainDB:Path)->dict:
    with open(pathToMainDB,'r') as dbFile:
        data = json.load(dbFile)

    return data

def loadIATADB()->dict:
    dbPath = Path("Python/resources/airportdb/iata_airports.json")
    airportDB = loadMainDB(dbPath)
    return airportDB

def filterOutNonIATAAirports(airportDB:dict)->dict:
    filteredDB:dict = dict()
    for key,value in airportDB.items():
        if value['iata'] is not "" and value['iata'] is not '0':
            if value['iata'] in filteredDB:
                logging.error(f"found duplicate IATA values, {value} and {filteredDB[value['iata']]}")
            filteredDB[value['iata']] = value
    return filteredDB

def saveAirportDB(savePath:Path,airportDB):
    with open(savePath,'w') as outFile:
        json.dump(airportDB,outFile,indent=2,sort_keys=False)

        