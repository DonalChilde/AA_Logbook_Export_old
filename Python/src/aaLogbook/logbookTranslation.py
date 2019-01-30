"""
TODO changed parse functions to support sending surrounding object, 
    in order to make more understandable log messages.
TODO build flight row dictionary for csv output.
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field,asdict
from dataclasses_json import dataclass_json, DataClassJsonMixin
from typing import List, Optional, Any,Dict
from datetime import timedelta, datetime, tzinfo
from aaLogbook.xmlTranslation import LogbookElement, YearElement, MonthElement, TripElement, DutyPeriodElement, FlightElement
from utilities.timedelta_util import parse_HHdotMM_To_timedelta
from utilities import json_util, csv_util
from airportsDB.airportsDB import load_airports_IATA_json
from pathlib import Path
# from dateutil import tz
# import uuid
import logging
import arrow
import json


#### setting up logger ####
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


@dataclass
class FlightRow:
    aaNumber: str = ''
    year: str = ''
    monthYear: str = ''
    sequenceNumber: str = ''
    sequenceStartDate: str = ''
    base: str = ''
    sequenceEquipmentType: str = ''
    uuid: str = ''
    flightNumber: str = ''
    departureStationIata: str = ''
    departureStationIcao: str = ''
    departureStationTz: str = ''
    outDateTimeUTC: str = ''
    outDateUTC: str=''
    outTimeUTC: str=''
    outDateTimeLCL: str = ''
    outDateLCL: str=''
    outTimeLCL: str=''
    arrivalStationIata: str = ''
    arrivalStationIcao: str = ''
    arrivalStationTz: str = ''
    inDateTimeUTC: str = ''
    inDateUTC: str=''
    inTimeUTC: str=''
    inDateTimeLCL: str = ''
    inDateLCL: str=''
    inTimeLCL: str=''
    fly: str = ''
    legGreater: str = ''
    actualBlock: str = ''
    groundTime: str = ''
    overnightDuration: str = ''
    eqModel: str = ''
    eqNumber: str = ''
    eqType: str = ''
    eqCode: str = ''
    fuelPerformance: str = ''
    departurePerformance: str = ''
    arrivalPerformance: str = ''
    position: str = ''
    delayCode: str = ''


@dataclass_json
@dataclass
class Station:
    iata: str = ""
    icao: str = ""
    timezone: str = ""


@dataclass_json
@dataclass
class Duration:
    hours: int = 0
    minutes: int = 0

    def to_timedelta(self)-> timedelta:
        return timedelta(hours=self.hours, minutes=self.minutes)


# @dataclass_json
@dataclass
class Logbook(DataClassJsonMixin):
    uuid: str = ""
    aaNumber: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    years: list = field(default_factory=list)


@dataclass_json
@dataclass
class Year:
    uuid: str = ""
    year: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    months: list = field(default_factory=list)


@dataclass_json
@dataclass
class Month:
    uuid: str = ""
    monthYear: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    trips: list = field(default_factory=list)


@dataclass_json
@dataclass
class Trip:
    uuid: str = ""
    startDate: str = ""
    sequenceNumber: str = ""
    base: str = ""
    equipmentType: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    dutyPeriods: list = field(default_factory=list)


@dataclass_json
@dataclass
class DutyPeriod:
    uuid: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    flights: list = field(default_factory=list)


@dataclass_json
@dataclass
class Flight:
    uuid: str = ""
    flightNumber: str = ""
    departureStation: Station = field(default_factory=Station)
    outDateTimeUTC: str = ""
    arrivalStation: Station = field(default_factory=Station)
    inDateTimeUTC: str = ""
    fly: Duration = field(default_factory=Duration)
    actualBlock: Duration = field(default_factory=Duration)
    legGreater: Duration = field(default_factory=Duration)
    eqModel: str = ""
    eqNumber: str = ""
    eqType: str = ""
    eqCode: str = ""
    groundTime: Duration = field(default_factory=Duration)
    overnightDuration: Duration = field(default_factory=Duration)
    fuelPerformance: str = ""
    departurePerformance: str = ""
    arrivalPerformance: str = ""
    position: str = ""
    delayCode: str = ""


def buildLogbook(logbookElement: LogbookElement)->Logbook:
    log = Logbook(uuid=logbookElement.uuid, aaNumber=logbookElement.aaNumber)
    for yearElement in logbookElement.years:
        year = buildYear(yearElement)
        # pylint: disable=E1101
        log.years.append(year)

    return log


def buildYear(yearElement: YearElement)->Year:
    year = Year(uuid=yearElement.uuid, year=yearElement.year)
    for monthElement in yearElement.months:
        month = buildMonth(monthElement)
        # pylint: disable=E1101
        year.months.append(month)
    return year


def buildMonth(monthElement: MonthElement)->Month:
    month = Month(uuid=monthElement.uuid, monthYear=monthElement.monthYear)
    for tripElement in monthElement.trips:
        trip = buildTrip(tripElement)
        # pylint: disable=E1101
        month.trips.append(trip)
    return month


def buildTrip(tripElement: TripElement)->Trip:
    startDate, sequenceNumber, base, equipmentType = splitTripInfo(
        tripElement.sequenceInfo)
    trip = Trip(uuid=tripElement.uuid, startDate=startDate,
                sequenceNumber=sequenceNumber, base=base, equipmentType=equipmentType)
    for dutyPeriodElement in tripElement.dutyPeriods:
        dutyPeriod = buildDutyPeriod(dutyPeriodElement)
        # pylint: disable=E1101
        trip.dutyPeriods.append(dutyPeriod)

    return trip


def buildDutyPeriod(dutyPeriodElement: DutyPeriodElement)->DutyPeriod:
    dutyPeriod = DutyPeriod(uuid=dutyPeriodElement.uuid)
    for flightElement in dutyPeriodElement.flights:
        flight = buildFlight(flightElement)
        # pylint: disable=E1101
        dutyPeriod.flights.append(flight)
    return dutyPeriod


def buildFlight(flightElement: FlightElement)->Flight:
    airportDB = load_airports_IATA_json()

    uuid = flightElement.uuid  # type: ignore
    flightNumber = flightElement.flightNumber
    departureStation = buildStation(flightElement.departureStation, airportDB)
    outDateTimeUTC = buildOutTime(
        flightElement.outDateTime, departureStation.timezone).to('utc')
    arrivalStation = buildStation(flightElement.arrivalStation, airportDB)
    fly = parse_HHdotMM_To_Duration(flightElement.fly)
    actualBlock = parse_HHdotMM_To_Duration(flightElement.actualBlock)
    legGreater = parse_HHdotMM_To_Duration(flightElement.legGreater)
    inDateTimeUTC = buildInTime(
        flightElement.inDateTime, actualBlock.to_timedelta(), outDateTimeUTC, arrivalStation.timezone).to('utc')
    eqModel = flightElement.eqModel
    eqNumber = flightElement.eqNumber
    eqType = flightElement.eqType
    eqCode = flightElement.eqCode
    groundTime = parse_HHdotMM_To_Duration(flightElement.groundTime)
    overnightDuration = parse_HHdotMM_To_Duration(
        flightElement.overnightDuration)
    fuelPerformance = flightElement.fuelPerformance
    departurePerformance = flightElement.departurePerformance
    arrivalPerformance = flightElement.arrivalPerformance
    position = flightElement.position
    delayCode = flightElement.delayCode

    flight = Flight(uuid=uuid,
                    flightNumber=flightNumber,
                    departureStation=departureStation,
                    outDateTimeUTC=outDateTimeUTC,
                    arrivalStation=arrivalStation,
                    fly=fly,
                    actualBlock=actualBlock,
                    legGreater=legGreater,
                    inDateTimeUTC=inDateTimeUTC,
                    eqModel=eqModel,
                    eqNumber=eqNumber,
                    eqType=eqType,
                    eqCode=eqCode,
                    groundTime=groundTime,
                    overnightDuration=overnightDuration,
                    fuelPerformance=fuelPerformance,
                    departurePerformance=departurePerformance,
                    arrivalPerformance=arrivalPerformance,
                    position=position,
                    delayCode=delayCode)
    return flight

def durationFormatterBasic(dur:Duration):
    return str(dur.to_timedelta())

def buildFlightRowDict(logbook: Logbook, durationFormatter: Optional[Any] = None)->List[Dict[str,str]]:
    if not durationFormatter:
        durationFormatter = durationFormatterBasic
    flightRows: List[Dict[str,str]] = []
    row = FlightRow()
    row.aaNumber = logbook.aaNumber
    for year in logbook.years:
        row.year = year.year
        for month in year.months:
            row.monthYear = month.monthYear
            for trip in month.trips:
                row.sequenceStartDate = trip.startDate
                row.sequenceNumber = trip.sequenceNumber
                row.sequenceEquipmentType = trip.equipmentType
                row.base = trip.base
                for dutyPeriod in trip.dutyPeriods:
                    for flight in dutyPeriod.flights:
                        row.uuid = flight.uuid
                        row.flightNumber = flight.flightNumber
                        row.departureStationIata = flight.departureStation.iata
                        row.departureStationIcao = flight.departureStation.icao
                        row.departureStationTz = flight.departureStation.timezone
                        row.outDateTimeUTC = flight.outDateTimeUTC
                        row.outDateUTC = flight.outDateTimeUTC.format('YYYY-MM-DD')
                        row.outTimeUTC = flight.outDateTimeUTC.format('HH:mm:ss')
                        row.outDateTimeLCL = flight.outDateTimeUTC.to(flight.departureStation.timezone)
                        row.outDateLCL = row.outDateTimeLCL.format('YYYY-MM-DD')
                        row.outTimeLCL = row.outDateTimeLCL.format('HH:mm:ss')
                        row.arrivalStationIata = flight.arrivalStation.iata
                        row.arrivalStationIcao = flight.arrivalStation.icao
                        row.arrivalStationTz = flight.arrivalStation.timezone
                        row.inDateTimeUTC = flight.inDateTimeUTC
                        row.inDateUTC = flight.inDateTimeUTC.format('YYYY-MM-DD')
                        row.inTimeUTC = flight.inDateTimeUTC.format('HH:mm:ss')
                        row.inDateTimeLCL = flight.inDateTimeUTC.to(flight.departureStation.timezone)
                        row.inDateLCL = row.inDateTimeLCL.format('YYYY-MM-DD')
                        row.inTimeLCL = row.inDateTimeLCL.format('HH:mm:ss')
                        row.fly = durationFormatter(flight.fly)
                        row.legGreater = durationFormatter(
                            flight.legGreater)
                        row.actualBlock = durationFormatter(
                            flight.actualBlock)
                        row.groundTime = durationFormatter(
                            flight.groundTime)
                        row.overnightDuration = durationFormatter(
                            flight.overnightDuration)
                        row.eqModel = flight.eqModel
                        row.eqNumber = flight.eqNumber
                        row.eqType = flight.eqType
                        row.eqCode = flight.eqCode
                        row.fuelPerformance = flight.fuelPerformance
                        row.departurePerformance = flight.departurePerformance
                        row.arrivalPerformance = flight.arrivalPerformance
                        row.position = flight.position
                        row.delayCode = flight.delayCode
                        flightRows.append(asdict(row))
    return flightRows



def parse_HHdotMM_To_Duration(durationString: str, separator: str = ".")-> Duration:
    """
    parses a string in the format "34.23", assuming HH.MM
    TODO input checking, no dot, minutes more than 59, include parent object in log message
    """
    if durationString:
        if not '.' in durationString:
            # logger.debug(
            #     f"Improperly formatted time sent to parse_HHdotMM_ToDuration, - {durationString} - Defaulting to 0 Duration")
            return Duration()
        hours, minutes = durationString.split(separator)
        duration = Duration(hours=int(hours), minutes=int(minutes))
        return duration
    else:
        return Duration()


def buildStation(iataCode: str, airportDB: dict)->Station:
    iataCap = iataCode.upper()
    icao = airportDB[iataCap]['icao']
    timezone = airportDB[iataCap]['tz']
    station = Station(iata=iataCap, icao=icao, timezone=timezone)
    return station


def buildOutTime(dateString: str, timeZoneString: str)-> arrow.Arrow:
    dt = arrow.get(dateString)
    dt2 = dt.replace(tzinfo=timeZoneString)
    return dt2


def buildInTime(inDateString: str, flightTime: timedelta, outDatetime: arrow.Arrow, inTimeZone: str)-> arrow.Arrow:

    inTime = outDatetime + flightTime
    # TODO check for use after change input to Arrow
    inDT = arrow.get(inTime).to(inTimeZone)
    return inDT


def splitTripInfo(sequenceInfo: str):
    # TODO not implemented yet
    return ("", "", "", "")


def save_logbookJson(logbookElement: LogbookElement, savePath: Path):
    # TODO change to handle Logbook instaed of LogbookElement
    logbook = buildLogbook(logbookElement)
    data = logbook.to_json()
    data = json.loads(data)
    json_util.saveJson(data, savePath)


def save_logbookCsv(logbook: Logbook, savePath: Path):
    flightRows = buildFlightRowDict(logbook)
    csv_util.writeDictToCsv(savePath,flightRows)
    

