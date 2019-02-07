"""
will provide interface for airport lookup.
load db to in memory sqlite? or just lookup from json.
simplest solution first, then play and do speed testing.

Data Source: https://github.com/mwgg/Airports
our airports http://ourairports.com/data/

TODO: https://python-packaging.readthedocs.io/en/latest/non-code-files.html
"""
import json
import logging
import click
from dataclasses import dataclass, asdict
import re
from pathlib import Path
from importlib import resources
from utilities.json_util import loadJson, saveJson
from utilities.csv_util import readCsv
from typing import List, Optional, Any, Dict


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


IATA_AIRPORTS_JSON = "openflights_airports_IATA.json"
AIRPORTS_JSON = "openflights_airports.json"
AIRPORTS_CSV = "openflights_airports.csv"


@dataclass
class Airport:
    # TODO post init processing for \N to None
    airport_id: str
    name: str
    city: str
    country: str
    iata: str
    icao: str
    latitude: str
    longitude: str
    altitude: str
    timezone_offset: str
    dst: str
    tz: str
    type_: str
    source: str

    def __post_init__(self):
        self.airport_id = self.translateNULL(self.airport_id)
        self.name = self.translateNULL(self.name)
        self.city = self.translateNULL(self.city)
        self.country = self.translateNULL(self.country)
        self.iata = self.translateNULL(self.iata)
        self.icao = self.translateNULL(self.icao)
        self.latitude = self.translateNULL(self.latitude)
        self.longitude = self.translateNULL(self.longitude)
        self.altitude = self.translateNULL(self.altitude)
        self.timezone_offset = self.translateNULL(self.timezone_offset)
        self.dst = self.translateNULL(self.dst)
        self.tz = self.translateNULL(self.tz)
        self.type_ = self.translateNULL(self.type_)
        self.source = self.translateNULL(self.source)

    def translateNULL(self, value: str) -> Optional[str]:
        if value == "\\N":
            return None
        else:
            return value


class AirportsDB:
    def __init__(self, pathToMainDB, pathToIATADB):
        self.pathToMainDB = pathToMainDB
        self.pathToIATADB = pathToIATADB


def load_airports_json() -> List[Dict[str, str]]:
    filePath = pathTo_airports_json()
    main_airportDB = loadJson(filePath)
    return main_airportDB


def load_airports_IATA_json() -> Dict[str, Dict[str, str]]:
    filePath = pathTo_airports_IATA_json()
    # TODO checks for existance, etc
    iata_airportDict = loadJson(filePath)
    return iata_airportDict


def load_OpenFLightsCSV(filePath: Path) -> List[Airport]:
    data = readCsv(filePath, Airport)
    return data


def pathTo_airports_IATA_json() -> Path:
    filePath: Optional[Path] = None
    try:
        with resources.path("airportsDB.data.airports", IATA_AIRPORTS_JSON) as iataPath:
            filePath = iataPath
    except FileNotFoundError:
        filePath = pathToDataDirectory() / Path(IATA_AIRPORTS_JSON)
        create_airports_IATA_json(filePath)
    return filePath


def pathTo_airports_json() -> Path:
    filePath: Optional[Path] = None
    try:
        with resources.path("airportsDB.data.airports", AIRPORTS_JSON) as iataPath:
            filePath = iataPath
    except FileNotFoundError:
        filePath = pathToDataDirectory() / Path(AIRPORTS_JSON)
        create_airports_json(filePath)
    return filePath


def pathTo_OpenFlightsCSV() -> Path:
    with resources.path("airportsDB.data.airports", AIRPORTS_CSV) as filePath:
        return filePath


def pathToDataDirectory() -> Path:
    with resources.path("airportsDB.data", "airports") as filePath:
        return filePath


def create_airports_IATA_json(path: Path):
    csvPath = pathTo_OpenFlightsCSV()
    airports = load_OpenFLightsCSV(csvPath)
    filtered = filter_Non_IATA_Airports(airports)
    iataDict = build_IATA_dict(filtered)
    saveJson(iataDict, path)


def create_airports_json(path: Path):
    csvPath = pathTo_OpenFlightsCSV()
    airports = load_OpenFLightsCSV(csvPath)
    airportsDict = [asdict(airport) for airport in airports]
    saveJson(airportsDict, path)


def validateAirport(airports: List[Airport]):
    """
    TODO validate Airport Fields
    """
    raise NotImplementedError


def build_IATA_dict(airports: List[Airport]) -> Dict[str, Dict[str, str]]:
    data: dict = {}
    for airport in airports:
        iataCode = airport.iata
        airportDict = asdict(airport)
        if iataCode in data:
            logging.error(
                f"found duplicate IATA values, {airportDict} overwrites {data[iataCode]}"
            )
        if not iataCode.isupper():
            logging.error(
                f"IATA code {iataCode}  for entry {airportDict} was not uppercase. converting to uppercase."
            )
            iataCode = iataCode.upper()
        if iataCode in data:
            logging.error(
                f"found duplicate IATA values, {airportDict} overwrites {data[iataCode]}"
            )
        data[iataCode] = airportDict
    return data


def filter_Non_IATA_Airports(airports: List[Airport]) -> List[Airport]:
    filtered: List[Airport] = []
    for airport in airports:
        if validateIATA_Code(airport.iata):
            filtered.append(airport)
    return filtered


def validateIATA_Code(iata: str) -> bool:
    if not isinstance(iata, str):
        return False
    iataRE = re.compile("[a-zA-Z]{3,3}")
    if iataRE.match(iata):
        return True
    else:
        return False


def maincli():
    pass


if __name__ == "__main__":
    maincli()
