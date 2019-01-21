"""
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
from datetime import timedelta, datetime, tzinfo
from xmlTranslation import LogbookElement, YearElement, MonthElement, TripElement, DutyPeriodElement, FlightElement
from timeDelta import parse_HHdotMM_ToTimeDelta
# from dateutil import tz
import uuid


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
        return timedelta(hours=self.hours,minutes=self.minutes)

@dataclass_json
@dataclass
class Logbook(object):
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    aaNumber: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    years: list = field(default_factory=list)


@dataclass_json
@dataclass
class Year:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    year: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    months: list = field(default_factory=list)


@dataclass_json
@dataclass
class Month:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    monthYear: str = ""
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    trips: list = field(default_factory=list)


@dataclass_json
@dataclass
class Trip:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
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
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    sumOfActualBlock: Duration = field(default_factory=Duration)
    sumOfLegGreater: Duration = field(default_factory=Duration)
    sumOfFly: Duration = field(default_factory=Duration)
    flights: list = field(default_factory=list)


@dataclass_json
@dataclass
class Flight:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
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
    uuid = flightElement.uuid
    flightNumber = flightElement.uuid
    departureStation = buildStation(flightElement.departureStation)
    outDateTimeUTC = buildOutTime(
        flightElement.outDateTime, departureStation.timezone)
    arrivalStation = buildStation(flightElement.arrivalStation)
    fly = parse_HHdotMM_ToDuration(flightElement.fly)
    actualBlock = parse_HHdotMM_ToDuration(flightElement.actualBlock)
    legGreater = parse_HHdotMM_ToDuration(flightElement.legGreater)
    inDateTimeUTC = buildInTime(flightElement.inDateTime, actualBlock.to_timedelta())
    eqModel = flightElement.eqModel
    eqNumber = flightElement.eqNumber
    eqType = flightElement.eqType
    eqCode = flightElement.eqCode
    groundTime = parse_HHdotMM_ToDuration(flightElement.groundTime)
    overnightDuration = parse_HHdotMM_ToDuration(
        flightElement.overnightDuration)
    fuelPerformance = flightElement.fuelPerformance
    departurePerformance = flightElement.departurePerformance
    arrivalPerformance = flightElement.arrivalPerformance
    position = flightElement.position
    delayCode = flightElement.delayCode

    flight = Flight(uuid=uuid,
                    flightNumber=flightNumber,
                    departureStation=departureStation,
                    outDateTimeUTC=outDateTimeUTC.isoformat(),
                    arrivalStation=arrivalStation,
                    fly=fly,
                    actualBlock=actualBlock,
                    legGreater=legGreater,
                    inDateTimeUTC=inDateTimeUTC.isoformat(),
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

def parse_HHdotMM_ToDuration(durationString:str,separator:str = ".")-> Duration:
    """
    parses a string in the format "34.23", assuming HH.MM
    """
    hours, minutes = durationString.split(separator)
    duration = Duration(hours=int(hours),minutes = int(minutes))
    return duration

def buildStation(iataCode: str)->Station:
    return Station()


def buildOutTime(dateString: str, timeZoneString: str)-> datetime:
    return datetime.now()


def buildInTime(dateString: str, flightTime: timedelta)-> datetime:
    return datetime.now()


def splitTripInfo(sequenceInfo: str):
    return ("", "", "", "")
