"""
"""
# TODO change uuid to be the string of entire data field, at least for flight.
#       this is to allow for differential exports for same logbook.
#       maybe make it a function on the FlightElement class, to support removing the
#       default uuid required to support typechecking. or change uuid to be a string type. <- this
# TODO add uuid generator to all Element classes, to be called one time after data parsing.
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
from dataclasses import dataclass, field, asdict as dc_asdict
from dataclasses_json import dataclass_json
from typing import List, Dict, Sequence, NamedTuple, Optional
from datetime import timedelta
from utilities import json_util, csv_util
import aaLogbook.models.xmlElementModel as xem
import uuid
import xml.etree.ElementTree as ET
import click
import json

# from sys import stdout


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
logger.addHandler(log_handler)

ns = {"crystal_reports": "urn:crystal-reports:schemas:report-detail"}


def parseXML(path):
    # print(path.resolve())
    with open(path, "r") as xmlFile:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        logbook = xem.LogbookElement()
        logbook.aaNumber = root.find(
            './crystal_reports:ReportHeader/crystal_reports:Section/crystal_reports:Field[@Name="EmpNum1"]/crystal_reports:Value',
            ns,
        ).text
        logbook.sumOfActualBlock = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock4"]/crystal_reports:Value',
            ns,
        ).text
        logbook.sumOfLegGreater = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr4"]/crystal_reports:Value',
            ns,
        ).text
        logbook.sumOfFly = root.find(
            './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly4"]/crystal_reports:Value',
            ns,
        ).text

        for item in root.findall("crystal_reports:Group", ns):
            # pylint: disable=E1101
            logbook.years.append(handleYear(item))
        return logbook


def handleYear(yearElement):
    # print('made it to year')
    year = xem.YearElement()
    year.year = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text34"]/crystal_reports:TextValue',
        ns,
    ).text
    year.sumOfActualBlock = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock6"]/crystal_reports:Value',
        ns,
    ).text
    year.sumOfLegGreater = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr6"]/crystal_reports:Value',
        ns,
    ).text
    year.sumOfFly = yearElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly6"]/crystal_reports:Value',
        ns,
    ).text

    for item in yearElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        year.months.append(handleMonth(item))
    validateYear(year, yearElement)

    return year


def handleMonth(monthElement):
    # print('made it to month')
    month = xem.MonthElement()
    month.monthYear = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text35"]/crystal_reports:TextValue',
        ns,
    ).text
    month.sumOfActualBlock = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock2"]/crystal_reports:Value',
        ns,
    ).text
    month.sumOfLegGreater = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr2"]/crystal_reports:Value',
        ns,
    ).text
    month.sumOfFly = monthElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly2"]/crystal_reports:Value',
        ns,
    ).text

    for item in monthElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        month.trips.append(handleTrip(item))
    validateMonth(month, monthElement)
    return month


def handleTrip(tripElement):
    # print('made it to trip')
    trip = xem.TripElement()
    trip.sequenceInfo = tripElement.find(
        './crystal_reports:GroupHeader/crystal_reports:Section/crystal_reports:Text[@Name="Text10"]/crystal_reports:TextValue',
        ns,
    ).text
    trip.sumOfActualBlock = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock3"]/crystal_reports:Value',
        ns,
    ).text
    trip.sumOfLegGreater = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr3"]/crystal_reports:Value',
        ns,
    ).text
    trip.sumOfFly = tripElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly3"]/crystal_reports:Value',
        ns,
    ).text

    for item in tripElement.findall("crystal_reports:Group", ns):
        # pylint: disable=E1101
        trip.dutyPeriods.append(handleDutyPeriod(item))
    validateTrip(trip, tripElement)
    return trip


def handleDutyPeriod(dutyPeriodElement):
    # print('made it to dp')
    dutyPeriod = xem.DutyPeriodElement()
    dutyPeriod.sumOfActualBlock = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock1"]/crystal_reports:Value',
        ns,
    ).text
    dutyPeriod.sumOfLegGreater = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr1"]/crystal_reports:Value',
        ns,
    ).text
    dutyPeriod.sumOfFly = dutyPeriodElement.find(
        './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly1"]/crystal_reports:Value',
        ns,
    ).text

    for item in dutyPeriodElement.findall("crystal_reports:Details", ns):
        # pylint: disable=E1101
        dutyPeriod.flights.append(handleFlight(item))
    # print(dutyPeriod)
    validateDutyPeriod(dutyPeriod, dutyPeriodElement)
    return dutyPeriod


def handleFlight(flightElement):
    # print('made it to flight')
    # print(flightElement.findall('.'))
    flight = xem.FlightElement()
    # flight.flightNumber = flightElement.find('./{urn:crystal-reports:schemas:report-detail}Section/{urn:crystal-reports:schemas:report-detail}Field/{urn:crystal-reports:schemas:report-detail}Value').text
    flight.flightNumber = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Flt1"]/crystal_reports:Value',
        ns,
    ).text
    flight.departureStation = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DepSta1"]/crystal_reports:Value',
        ns,
    ).text
    flight.outDateTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="OutDtTime1"]/crystal_reports:Value',
        ns,
    ).text
    flight.arrivalStation = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ArrSta1"]/crystal_reports:Value',
        ns,
    ).text
    flight.fly = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Fly1"]/crystal_reports:Value',
        ns,
    ).text
    flight.legGreater = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="LegGtr1"]/crystal_reports:Value',
        ns,
    ).text
    flight.eqModel = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Model1"]/crystal_reports:Value',
        ns,
    ).text
    flight.eqNumber = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="AcNum1"]/crystal_reports:Value',
        ns,
    ).text
    flight.eqType = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="EQType1"]/crystal_reports:Value',
        ns,
    ).text
    flight.eqCode = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="LeqEq1"]/crystal_reports:Value',
        ns,
    ).text
    flight.groundTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="Grd1"]/crystal_reports:Value',
        ns,
    ).text
    flight.overnightDuration = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DpActOdl1"]/crystal_reports:Value',
        ns,
    ).text
    flight.fuelPerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="FuelPerf1"]/crystal_reports:Value',
        ns,
    ).text
    flight.departurePerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DepPerf1"]/crystal_reports:Value',
        ns,
    ).text
    flight.arrivalPerformance = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ArrPerf1"]/crystal_reports:Value',
        ns,
    ).text
    flight.actualBlock = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ActualBlock1"]/crystal_reports:Value',
        ns,
    ).text
    flight.position = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="ActulaPos1"]/crystal_reports:Value',
        ns,
    ).text
    flight.delayCode = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="DlyCode1"]/crystal_reports:Value',
        ns,
    ).text
    flight.inDateTime = flightElement.find(
        './crystal_reports:Section/crystal_reports:Field[@Name="InDateTimeOrMins1"]/crystal_reports:Value',
        ns,
    ).text
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


def buildFlightRows(logbook: xem.LogbookElement) -> List[Dict[str, str]]:
    flightRows: List[Dict[str, str]] = []
    logbookFields = {"aaNumber": logbook.aaNumber}
    for year in logbook.years:
        yearFields = {"year": year.year}
        for month in year.months:
            monthFields = {"monthYear": month.monthYear}
            for trip in month.trips:
                tripFields = {"sequenceInfo": trip.sequenceInfo}
                for dutyPeriod in trip.dutyPeriods:
                    for flight in dutyPeriod.flights:
                        flightFields = dc_asdict(flight)
                        flightFields.update(logbookFields)
                        flightFields.update(yearFields)
                        flightFields.update(monthFields)
                        flightFields.update(tripFields)
                        # flightRow = FlightRow(**flightFields)
                        flightRows.append(flightFields)
    return flightRows


def saveRawJson(xmlPath: Path, savePath: Path):
    logbook = parseXML(xmlPath)
    data = logbook.to_json()  # pylint: disable=E1101
    data = json.loads(data)
    json_util.saveJson(data, savePath)


def saveRawFlatJson(xmlPath: Path, savePath: Path):
    logbook = parseXML(xmlPath)
    flightRows = buildFlightRows(logbook)
    json_util.saveJson(flightRows, savePath)


def saveRawCsv(xmlPath: Path, savePath: Path):
    # TODO selectable save fields
    logbook = parseXML(xmlPath)
    flightRows = buildFlightRows(logbook)
    fieldList = (
        "aaNumber",
        "year",
        "monthYear",
        "sequenceInfo",
        "uuid",
        "flightNumber",
        "departureStation",
        "outDateTime",
        "arrivalStation",
        "inDateTime",
        "fly",
        "legGreater",
        "actualBlock",
        "groundTime",
        "overnightDuration",
        "eqModel",
        "eqNumber",
        "eqType",
        "eqCode",
        "fuelPerformance",
        "departurePerformance",
        "arrivalPerformance",
        "position",
        "delayCode",
    )
    csv_util.writeDictToCsv(savePath, flightRows, fieldList)
