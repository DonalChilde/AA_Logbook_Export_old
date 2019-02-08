"""
TODO changed parse functions to support sending surrounding object, 
    in order to make more understandable log messages.
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field, asdict
from dataclasses_json import dataclass_json, DataClassJsonMixin
from typing import List, Optional, Any, Dict, Sequence
from datetime import timedelta, datetime, tzinfo
from aaLogbook.models.xmlElementModel import (
    LogbookElement,
    YearElement,
    MonthElement,
    TripElement,
    DutyPeriodElement,
    FlightElement,
)
import aaLogbook.models.logbookTranslationModel as ltm
from utilities.timedelta_util import parse_HHdotMM_To_timedelta, timeDelta_TO_HHMMSS
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
    "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)
# log_handler = logging.StreamHandler(stdout)
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
# logger.addHandler(log_handler)


def buildLogbook(logbookElement: LogbookElement) -> ltm.Logbook:
    airportDB = load_airports_IATA_json()
    context = {"airportDB": airportDB}
    log = ltm.Logbook(uuid=logbookElement.uuid, aaNumber=logbookElement.aaNumber)
    for yearElement in logbookElement.years:
        year = buildYear(yearElement, context)
        # pylint: disable=no-member
        log.years.append(year)

    return log


def buildYear(yearElement: YearElement, context: Dict[str, Any]) -> ltm.Year:
    year = ltm.Year(uuid=yearElement.uuid, year=yearElement.year)
    for monthElement in yearElement.months:
        month = buildMonth(monthElement, context)
        # pylint: disable=no-member
        year.months.append(month)
    return year


def buildMonth(monthElement: MonthElement, context: Dict[str, Any]) -> ltm.Month:
    month = ltm.Month(uuid=monthElement.uuid, monthYear=monthElement.monthYear)
    for tripElement in monthElement.trips:
        trip = buildTrip(tripElement, context)
        # pylint: disable=no-member
        month.trips.append(trip)
    return month


def buildTrip(tripElement: TripElement, context: Dict[str, Any]) -> ltm.Trip:
    startDate, sequenceNumber, base, equipmentType = splitTripInfo(
        tripElement.sequenceInfo
    )
    trip = ltm.Trip(
        uuid=tripElement.uuid,
        startDate=startDate,
        sequenceNumber=sequenceNumber,
        base=base,
        equipmentType=equipmentType,
    )
    for dutyPeriodElement in tripElement.dutyPeriods:
        dutyPeriod = buildDutyPeriod(dutyPeriodElement, context)
        # pylint: disable=no-member
        trip.dutyPeriods.append(dutyPeriod)

    return trip


def buildDutyPeriod(
    dutyPeriodElement: DutyPeriodElement, context: Dict[str, Any]
) -> ltm.DutyPeriod:
    dutyPeriod = ltm.DutyPeriod(uuid=dutyPeriodElement.uuid)
    for flightElement in dutyPeriodElement.flights:
        flight = buildFlight(flightElement, context)
        # pylint: disable=no-member
        dutyPeriod.flights.append(flight)
    return dutyPeriod


def buildFlight(flightElement: FlightElement, context: Dict[str, Any]) -> ltm.Flight:
    airportDB = context["airportDB"]

    uuid = flightElement.uuid  # type: ignore
    flightNumber = flightElement.flightNumber
    departureStation = buildStation(flightElement.departureStation, airportDB)
    outDateTimeUTC = buildOutTimeUTC(
        flightElement.outDateTime, departureStation.timezone
    )
    arrivalStation = buildStation(flightElement.arrivalStation, airportDB)
    fly = parse_HHdotMM_To_Duration(flightElement.fly)
    actualBlock = parse_HHdotMM_To_Duration(flightElement.actualBlock)
    legGreater = parse_HHdotMM_To_Duration(flightElement.legGreater)
    inDateTimeUTC = buildInTimeUTC(
        flightElement.inDateTime,
        actualBlock.to_timedelta(),
        outDateTimeUTC,
        arrivalStation.timezone,
    )
    eqModel = flightElement.eqModel
    eqNumber = flightElement.eqNumber
    eqType = flightElement.eqType
    eqCode = flightElement.eqCode
    groundTime = parse_HHdotMM_To_Duration(flightElement.groundTime)
    overnightDuration = parse_HHdotMM_To_Duration(flightElement.overnightDuration)
    fuelPerformance = flightElement.fuelPerformance
    departurePerformance = flightElement.departurePerformance
    arrivalPerformance = flightElement.arrivalPerformance
    position = flightElement.position
    delayCode = flightElement.delayCode

    flight = ltm.Flight(
        uuid=uuid,
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
        delayCode=delayCode,
    )
    return flight


def durationFormatterBasic(dur: ltm.Duration):
    return timeDelta_TO_HHMMSS(dur.to_timedelta())


def buildFlightRowDict(
    logbook: ltm.Logbook, durationFormatter: Optional[Any] = None
) -> List[Dict[str, str]]:
    if not durationFormatter:
        durationFormatter = durationFormatterBasic
    flightRows: List[Dict[str, str]] = []
    row = ltm.FlightRow()
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
                for index, dutyPeriod in enumerate(trip.dutyPeriods):
                    row.dutyPeriodNumber = str(index + 1)
                    for flight in dutyPeriod.flights:
                        row.uuid = flight.uuid
                        row.flightNumber = flight.flightNumber
                        row.departureStationIata = flight.departureStation.iata
                        row.departureStationIcao = flight.departureStation.icao
                        row.departureStationTz = flight.departureStation.timezone
                        row.outDateTimeUTC = flight.outDateTimeUTC
                        row.outDateUTC = flight.outDateTimeUTC.format("YYYY-MM-DD")
                        row.outTimeUTC = flight.outDateTimeUTC.format("HH:mm:ss")
                        row.outDateTimeLCL = flight.outDateTimeUTC.to(
                            flight.departureStation.timezone
                        )
                        row.outDateLCL = row.outDateTimeLCL.format("YYYY-MM-DD")
                        row.outTimeLCL = row.outDateTimeLCL.format("HH:mm:ss")
                        row.arrivalStationIata = flight.arrivalStation.iata
                        row.arrivalStationIcao = flight.arrivalStation.icao
                        row.arrivalStationTz = flight.arrivalStation.timezone
                        row.inDateTimeUTC = flight.inDateTimeUTC
                        row.inDateUTC = flight.inDateTimeUTC.format("YYYY-MM-DD")
                        row.inTimeUTC = flight.inDateTimeUTC.format("HH:mm:ss")
                        row.inDateTimeLCL = flight.inDateTimeUTC.to(
                            flight.departureStation.timezone
                        )
                        row.inDateLCL = row.inDateTimeLCL.format("YYYY-MM-DD")
                        row.inTimeLCL = row.inDateTimeLCL.format("HH:mm:ss")
                        row.fly = durationFormatter(flight.fly)
                        row.legGreater = durationFormatter(flight.legGreater)
                        row.actualBlock = durationFormatter(flight.actualBlock)
                        row.groundTime = durationFormatter(flight.groundTime)
                        row.overnightDuration = durationFormatter(
                            flight.overnightDuration
                        )
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


def parse_HHdotMM_To_Duration(
    durationString: str, separator: str = "."
) -> ltm.Duration:
    """
    parses a string in the format "34.23", assuming HH.MM
    TODO input checking, no dot, minutes more than 59, include parent object in log message
    """
    if durationString:
        if not "." in durationString:
            # logger.debug(
            #     f"Improperly formatted time sent to parse_HHdotMM_ToDuration, - {durationString} - Defaulting to 0 Duration")
            return ltm.Duration()
        hours, minutes = durationString.split(separator)
        duration = ltm.Duration(hours=int(hours), minutes=int(minutes))
        return duration
    else:
        return ltm.Duration()


def buildStation(iataCode: str, airportDB: dict) -> ltm.Station:
    iataCap = iataCode.upper()
    icao = airportDB[iataCap]["icao"]
    timezone = airportDB[iataCap]["tz"]
    station = ltm.Station(iata=iataCap, icao=icao, timezone=timezone)
    return station


def buildOutTimeUTC(dateString: str, timeZoneString: str) -> arrow.Arrow:
    outTime = arrow.get(dateString)
    outTimeWithTZ = outTime.replace(tzinfo=timeZoneString)
    return outTimeWithTZ.to("utc")


def buildInTimeUTC(
    inDateString: str, flightTime: timedelta, outDatetime: arrow.Arrow, inTimeZone: str
) -> arrow.Arrow:
    inTimeUTC = outDatetime + flightTime
    # TODO do validation checks against partial datetime from inDateString

    return inTimeUTC


def splitTripInfo(sequenceInfo: str):
    # TODO do validation checks
    return sequenceInfo.split()


def save_logbookJson(logbook: ltm.Logbook, savePath: Path, parseContext: dict):
    data = logbook.to_json()
    data = json.loads(data)
    json_util.saveJson(data, savePath)


def save_logbookCsv(
    logbook: ltm.Logbook,
    savePath: Path,
    parseContext: dict,
    fieldList: Optional[Sequence[str]] = None,
):
    flightRows = buildFlightRowDict(logbook)
    csv_util.writeDictToCsv(savePath, flightRows, fieldList)
