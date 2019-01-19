"""
"""

# TODO data structure to hold parsed info
# TODO data structure to hold parsed info, as well as interpreted info.
# TODO output parsed info to csv
# TODO output interpreted info to csv
# TODO describe data format in readme
# TODO cmdline interface
# TODO flask interface

from __future__ import annotations
import logging
from pathlib import Path
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
from datetime import timedelta
import uuid


#from sys import stdout
import xml.etree.ElementTree as ET

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
logger.addHandler(log_handler)

ns = {'crystal_reports': 'urn:crystal-reports:schemas:report-detail'}

@dataclass_json
@dataclass
class Logbook(object):
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    aaNumber: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    years: list = field(default_factory=list)
    
@dataclass_json
@dataclass
class Year:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    year: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    months: list = field(default_factory=list)


@dataclass_json
@dataclass
class Month:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    monthYear: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    trips: list = field(default_factory=list)


@dataclass_json
@dataclass
class Trip:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    sequenceInfo: str = ""
    startDate: str = ""
    sequenceNumber: str = ""
    base: str = ""
    equipmentType:str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    dutyPeriods: list = field(default_factory=list)


@dataclass_json
@dataclass
class DutyPeriod:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    flights: list = field(default_factory=list)


@dataclass_json
@dataclass
class Flight:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    flightNumber: str = ""
    departureStation: str = ""
    outDateTime: str = ""
    arrivalStation: str = ""
    fly: str = ""
    legGreater: str = ""
    eqModel: str = ""
    eqNumber: str = ""
    eqType: str = ""
    eqCode: str = ""
    groundTime: str = ""
    overnightDuration: str = ""
    fuelPerformance: str = ""
    departurePerformance: str = ""
    arrivalPerformance: str = ""
    actualBlock: str = ""
    position: str = ""
    delayCode: str = ""
    inDateTime: str = ""


@dataclass_json
@dataclass
class LogbookElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    aaNumber: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    years: list = field(default_factory=list)


@dataclass_json
@dataclass
class YearElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    year: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    months: list = field(default_factory=list)


@dataclass_json
@dataclass
class MonthElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    monthYear: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    trips: list = field(default_factory=list)


@dataclass_json
@dataclass
class TripElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    sequenceInfo: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    dutyPeriods: list = field(default_factory=list)


@dataclass_json
@dataclass
class DutyPeriodElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    flights: list = field(default_factory=list)


@dataclass_json
@dataclass
class FlightElement:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4) #type: ignore
    flightNumber: str = ""
    departureStation: str = ""
    outDateTime: str = ""
    arrivalStation: str = ""
    fly: str = ""
    legGreater: str = ""
    eqModel: str = ""
    eqNumber: str = ""
    eqType: str = ""
    eqCode: str = ""
    groundTime: str = ""
    overnightDuration: str = ""
    fuelPerformance: str = ""
    departurePerformance: str = ""
    arrivalPerformance: str = ""
    actualBlock: str = ""
    position: str = ""
    delayCode: str = ""
    inDateTime: str = ""


def parseXML(path):
    # print(path.resolve())
    with open(path, 'r') as xmlFile:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        print('root:', root.tag)
        logbook = LogbookElement()
        logbook.aaNumber = root.find(
            './crystal_reports:ReportHeader/crystal_reports:Section/crystal_reports:Field[@Name="EmpNum1"]/crystal_reports:Value', ns).text
        logbook.sumOfActualBlock = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock4"]/crystal_reports:Value', ns).text
        logbook.sumOfLegGreater = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr4"]/crystal_reports:Value', ns).text
        logbook.sumOfFly = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly4"]/crystal_reports:Value', ns).text

        for item in root.findall("crystal_reports:Group", ns):
            # pylint: disable=E1101
            logbook.years.append(handleYear(item))
        return logbook


def handleYear(yearElement):
    # print('made it to year')
    year = YearElement()
    year.year = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text34"]/crystal_reports:TextValue', ns).text
    year.sumOfActualBlock = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock6"]/crystal_reports:Value', ns).text
    year.sumOfLegGreater = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr6"]/crystal_reports:Value', ns).text
    year.sumOfFly = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly6"]/crystal_reports:Value', ns).text

    for item in yearElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        year.months.append(handleMonth(item))
    validateYear(year, yearElement)

    return year


def handleMonth(monthElement):
    # print('made it to month')
    month = MonthElement()
    month.monthYear = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text35"]/crystal_reports:TextValue', ns).text
    month.sumOfActualBlock = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock2"]/crystal_reports:Value', ns).text
    month.sumOfLegGreater = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr2"]/crystal_reports:Value', ns).text
    month.sumOfFly = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly2"]/crystal_reports:Value', ns).text

    for item in monthElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        month.trips.append(handleTrip(item))
    validateMonth(month, monthElement)
    return month


def handleTrip(tripElement):
    # print('made it to trip')
    trip = TripElement()
    trip.sequenceInfo = tripElement.find(
        './crystal_reports:GroupHeader/crystal_reports:Section/crystal_reports:Text[@Name="Text10"]/crystal_reports:TextValue', ns).text
    trip.sumOfActualBlock = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock3"]/crystal_reports:Value', ns).text
    trip.sumOfLegGreater = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr3"]/crystal_reports:Value', ns).text
    trip.sumOfFly = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly3"]/crystal_reports:Value', ns).text

    for item in tripElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        trip.dutyPeriods.append(handleDutyPeriod(item)
                                )
    validateTrip(trip, tripElement)
    return trip


def handleDutyPeriod(dutyPeriodElement):
    # print('made it to dp')
    dutyPeriod = DutyPeriodElement()
    dutyPeriod.sumOfActualBlock = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock1"]/crystal_reports:Value', ns).text
    dutyPeriod.sumOfLegGreater = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr1"]/crystal_reports:Value', ns).text
    dutyPeriod.sumOfFly = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly1"]/crystal_reports:Value', ns).text

    for item in dutyPeriodElement.findall("crystal_reports:Details", ns):
        # pylint: disable=E1101
        dutyPeriod.flights.append(handleFlight(item))
    # print(dutyPeriod)
    validateDutyPeriod(dutyPeriod, dutyPeriodElement)
    return dutyPeriod


def handleFlight(flightElement):
    # print('made it to flight')
    # print(flightElement.findall('.'))
    flight = FlightElement()
    # flight.flightNumber = flightElement.find('./{urn:crystal-reports:schemas:report-detail}Section/{urn:crystal-reports:schemas:report-detail}Field/{urn:crystal-reports:schemas:report-detail}Value').text
    flight.flightNumber = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Flt1"]/crystal_reports:Value', ns).text
    flight.departureStation = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DepSta1"]/crystal_reports:Value', ns).text
    flight.outDateTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="OutDtTime1"]/crystal_reports:Value', ns).text
    flight.arrivalStation = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ArrSta1"]/crystal_reports:Value', ns).text
    flight.fly = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Fly1"]/crystal_reports:Value', ns).text
    flight.legGreater = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="LegGtr1"]/crystal_reports:Value', ns).text
    flight.eqModel = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Model1"]/crystal_reports:Value', ns).text
    flight.eqNumber = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="AcNum1"]/crystal_reports:Value', ns).text
    flight.eqType = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="EQType1"]/crystal_reports:Value', ns).text
    flight.eqCode = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="LeqEq1"]/crystal_reports:Value', ns).text
    flight.groundTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Grd1"]/crystal_reports:Value', ns).text
    flight.overnightDuration = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DpActOdl1"]/crystal_reports:Value', ns).text
    flight.fuelPerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="FuelPerf1"]/crystal_reports:Value', ns).text
    flight.departurePerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DepPerf1"]/crystal_reports:Value', ns).text
    flight.arrivalPerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ArrPerf1"]/crystal_reports:Value', ns).text
    flight.actualBlock = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ActualBlock1"]/crystal_reports:Value', ns).text
    flight.position = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ActulaPos1"]/crystal_reports:Value', ns).text
    flight.delayCode = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DlyCode1"]/crystal_reports:Value', ns).text
    flight.inDateTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="InDateTimeOrMins1"]/crystal_reports:Value', ns).text
    validateFlight(flight, flightElement)
    return flight


def validateYear(year, yearElement):
    pass


def validateMonth(month, monthElement):
    pass


def validateTrip(trip, tripElement):
    pass


def validateDutyPeriod(dutyPeriod, dutyPeriodElement):
    pass


def validateFlight(flight, flightElement):
    pass


def parse_HHdotMM_ToTimeDelta(durationString)-> timedelta:
    hours, minutes = durationString.split('.')
    hours, minutes = map(int, (hours, minutes))
    return timedelta(hours=hours, minutes=minutes)


def timeDeltaToIsoString(timeDelta: timedelta)-> str:
    seconds = timeDelta.total_seconds()
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    hours, minutes = map(int, (hours, minutes))
    seconds = round(seconds)
    isoString = f"PT{hours}H{minutes}M{seconds}S"
    return isoString

# def iso8601(timeDelta: timedelta):
#     """
#     from:
#     https://stackoverflow.com/questions/27168175/convert-a-datetime-timedelta-into-iso-8601-duration-in-python
#     """
#     # split seconds to larger units
#     seconds = timeDelta.total_seconds()
#     minutes, seconds = divmod(seconds, 60)
#     hours, minutes = divmod(minutes, 60)
#     days, hours = divmod(hours, 24)
#     days, hours, minutes = map(int, (days, hours, minutes))
#     seconds = round(seconds, 6)

#     ## build date
#     date = ''
#     if days:
#         date = '%sD' % days

#     ## build time
#     time = u'T'
#     # hours
#     bigger_exists = date or hours
#     if bigger_exists:
#         time += '{:02}H'.format(hours)
#     # minutes
#     bigger_exists = bigger_exists or minutes
#     if bigger_exists:
#       time += '{:02}M'.format(minutes)
#     # seconds
#     if seconds.is_integer():
#         seconds = '{:02}'.format(int(seconds))
#     else:
#         # 9 chars long w/leading 0, 6 digits after decimal
#         seconds = '%09.6f' % seconds
#     # remove trailing zeros
#     seconds = seconds.rstrip('0')
#     time += '{}S'.format(seconds)
#     return u'P' + date + time
