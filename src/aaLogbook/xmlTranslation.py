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
from typing import List, Dict, Sequence, NamedTuple, Optional, Any
from datetime import timedelta
from utilities import json_util, csv_util
from utilities.str_util import safeStrip
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


def parseXML(path, parseContext):
    # print(path.resolve())
    with open(path, "r") as xmlFile:
        tree = ET.parse(xmlFile)
        root = tree.getroot()
        logbook = xem.LogbookElement()
        logbook.aaNumber = safeStrip(
            root.find(
                './crystal_reports:ReportHeader/crystal_reports:Section/crystal_reports:Field[@Name="EmpNum1"]/crystal_reports:Value',
                ns,
            ).text
        )
        logbook.sumOfActualBlock = safeStrip(
            root.find(
                './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock4"]/crystal_reports:Value',
                ns,
            ).text
        )
        logbook.sumOfLegGreater = safeStrip(
            root.find(
                './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr4"]/crystal_reports:Value',
                ns,
            ).text
        )
        logbook.sumOfFly = safeStrip(
            root.find(
                './crystal_reports:ReportFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly4"]/crystal_reports:Value',
                ns,
            ).text
        )
        parseContext["xmlparse"] = {}

        for item in root.findall("crystal_reports:Group", ns):
            # pylint: disable=no-member
            logbook.years.append(handleYear(item, parseContext))
        return logbook


def logbookStats(logbook: xem.LogbookElement, parseContext: dict):
    """
    Logbook: total times in the 3 duration fields, total months, total dutyperiods
        total flights, total dh flights,total overnights, nights at each station.
    year:
    month:
    dutyperiod:
    flight:
    """
    pass


def handleYear(yearElement, parseContext):
    # print('made it to year')
    year = xem.YearElement()
    year.year = safeStrip(
        yearElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text34"]/crystal_reports:TextValue',
            ns,
        ).text
    )
    year.sumOfActualBlock = safeStrip(
        yearElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock6"]/crystal_reports:Value',
            ns,
        ).text
    )
    year.sumOfLegGreater = safeStrip(
        yearElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr6"]/crystal_reports:Value',
            ns,
        ).text
    )
    year.sumOfFly = safeStrip(
        yearElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly6"]/crystal_reports:Value',
            ns,
        ).text
    )

    for item in yearElement.findall("crystal_reports:Group", ns):
        # pylint: disable=no-member
        year.months.append(handleMonth(item, parseContext))
    validateYear(year, yearElement)

    return year


def handleMonth(monthElement, parseContext):
    # print('made it to month')
    month = xem.MonthElement()
    month.monthYear = safeStrip(
        monthElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Text[@Name="Text35"]/crystal_reports:TextValue',
            ns,
        ).text
    )
    month.sumOfActualBlock = safeStrip(
        monthElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock2"]/crystal_reports:Value',
            ns,
        ).text
    )
    month.sumOfLegGreater = safeStrip(
        monthElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr2"]/crystal_reports:Value',
            ns,
        ).text
    )
    month.sumOfFly = safeStrip(
        monthElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly2"]/crystal_reports:Value',
            ns,
        ).text
    )

    for item in monthElement.findall("crystal_reports:Group", ns):
        # pylint: disable=no-member
        month.trips.append(handleTrip(item, parseContext))
    validateMonth(month, monthElement)
    return month


def handleTrip(tripElement, parseContext):
    # print('made it to trip')
    trip = xem.TripElement()
    trip.sequenceInfo = safeStrip(
        tripElement.find(
            './crystal_reports:GroupHeader/crystal_reports:Section/crystal_reports:Text[@Name="Text10"]/crystal_reports:TextValue',
            ns,
        ).text
    )
    trip.sumOfActualBlock = safeStrip(
        tripElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock3"]/crystal_reports:Value',
            ns,
        ).text
    )
    trip.sumOfLegGreater = safeStrip(
        tripElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr3"]/crystal_reports:Value',
            ns,
        ).text
    )
    trip.sumOfFly = safeStrip(
        tripElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly3"]/crystal_reports:Value',
            ns,
        ).text
    )

    for item in tripElement.findall("crystal_reports:Group", ns):
        # pylint: disable=no-member
        trip.dutyPeriods.append(handleDutyPeriod(item, parseContext))
    validateTrip(trip, tripElement)
    return trip


def handleDutyPeriod(dutyPeriodElement, parseContext):
    # print('made it to dp')
    dutyPeriod = xem.DutyPeriodElement()
    dutyPeriod.sumOfActualBlock = safeStrip(
        dutyPeriodElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofActualBlock1"]/crystal_reports:Value',
            ns,
        ).text
    )
    dutyPeriod.sumOfLegGreater = safeStrip(
        dutyPeriodElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofLegGtr1"]/crystal_reports:Value',
            ns,
        ).text
    )
    dutyPeriod.sumOfFly = safeStrip(
        dutyPeriodElement.find(
            './crystal_reports:GroupFooter/crystal_reports:Section/crystal_reports:Field[@Name="SumofFly1"]/crystal_reports:Value',
            ns,
        ).text
    )

    for item in dutyPeriodElement.findall("crystal_reports:Details", ns):
        # pylint: disable=no-member
        dutyPeriod.flights.append(handleFlight(item, parseContext))
    # print(dutyPeriod)
    validateDutyPeriod(dutyPeriod, dutyPeriodElement)
    return dutyPeriod


def handleFlight(flightElement, parseContext):
    # print('made it to flight')
    # print(flightElement.findall('.'))
    flight = xem.FlightElement()
    # flight.flightNumber = flightElement.find('./{urn:crystal-reports:schemas:report-detail}Section/{urn:crystal-reports:schemas:report-detail}Field/{urn:crystal-reports:schemas:report-detail}Value').text)
    flight.flightNumber = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="Flt1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.departureStation = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="DepSta1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.outDateTime = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="OutDtTime1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.arrivalStation = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="ArrSta1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.fly = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="Fly1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.legGreater = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="LegGtr1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.eqModel = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="Model1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.eqNumber = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="AcNum1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.eqType = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="EQType1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.eqCode = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="LeqEq1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.groundTime = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="Grd1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.overnightDuration = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="DpActOdl1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.fuelPerformance = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="FuelPerf1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.departurePerformance = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="DepPerf1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.arrivalPerformance = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="ArrPerf1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.actualBlock = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="ActualBlock1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.position = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="ActulaPos1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.delayCode = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="DlyCode1"]/crystal_reports:Value',
            ns,
        ).text
    )
    flight.inDateTime = safeStrip(
        flightElement.find(
            './crystal_reports:Section/crystal_reports:Field[@Name="InDateTimeOrMins1"]/crystal_reports:Value',
            ns,
        ).text
    )
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


def saveRawJson(xmlPath: Path, savePath: Path, parseContext: dict):

    logbook = parseXML(xmlPath, parseContext)
    data = logbook.to_json()  # pylint: disable=no-member
    data = json.loads(data)
    json_util.saveJson(data, savePath)


def saveRawFlatJson(xmlPath: Path, savePath: Path, parseContext: dict):
    logbook = parseXML(xmlPath, parseContext)
    flightRows = buildFlightRows(logbook)
    json_util.saveJson(flightRows, savePath)


def saveRawCsv(xmlPath: Path, savePath: Path, parseContext: dict):
    # TODO selectable save fields
    logbook = parseXML(xmlPath, parseContext)
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
