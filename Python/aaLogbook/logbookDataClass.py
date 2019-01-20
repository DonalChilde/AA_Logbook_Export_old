"""
"""

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List
from datetime import timedelta,datetime,tzinfo
# from dateutil import tz
import uuid

@dataclass_json
@dataclass
class Station:
    iata: str = ""
    icao: str = ""
    timezone:str = ""

@dataclass_json
@dataclass
class Logbook(object):
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    aaNumber: str = ""
    sumOfActualBlock: timedelta = field(default_factory=timedelta)
    sumOfLegGreater: timedelta = field(default_factory=timedelta)
    sumOfFly: timedelta = field(default_factory=timedelta)
    years: list = field(default_factory=list)


@dataclass_json
@dataclass
class Year:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    year: str = ""
    sumOfActualBlock: timedelta = field(default_factory=timedelta)
    sumOfLegGreater: timedelta = field(default_factory=timedelta)
    sumOfFly: timedelta = field(default_factory=timedelta)
    months: list = field(default_factory=list)


@dataclass_json
@dataclass
class Month:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    monthYear: str = ""
    sumOfActualBlock: timedelta = field(default_factory=timedelta)
    sumOfLegGreater: timedelta = field(default_factory=timedelta)
    sumOfFly: timedelta = field(default_factory=timedelta)
    trips: list = field(default_factory=list)


@dataclass_json
@dataclass
class Trip:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    startDate: str = ""
    sequenceNumber: str = ""
    base: str = ""
    equipmentType: str = ""
    sumOfActualBlock: timedelta = field(default_factory=timedelta)
    sumOfLegGreater: timedelta = field(default_factory=timedelta)
    sumOfFly: timedelta = field(default_factory=timedelta)
    dutyPeriods: list = field(default_factory=list)


@dataclass_json
@dataclass
class DutyPeriod:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    sumOfActualBlock: timedelta = field(default_factory=timedelta)
    sumOfLegGreater: timedelta = field(default_factory=timedelta)
    sumOfFly: timedelta = field(default_factory=timedelta)
    flights: list = field(default_factory=list)


@dataclass_json
@dataclass
class Flight:
    uuid: uuid.UUID = field(default_factory=uuid.uuid4)  # type: ignore
    flightNumber: Station = field(default_factory=Station)
    departureStation: str = ""
    outDateTimeUTC: str = ""
    arrivalStation: Station = field(default_factory=Station)
    inDateTimeUTC: str = ""
    fly: str = ""
    actualBlock: timedelta = field(default_factory=timedelta)
    legGreater: timedelta = field(default_factory=timedelta)
    eqModel: str = ""
    eqNumber: str = ""
    eqType: str = ""
    eqCode: str = ""
    groundTime: timedelta = field(default_factory=timedelta)
    overnightDuration: timedelta = field(default_factory=timedelta)
    fuelPerformance: str = ""
    departurePerformance: str = ""
    arrivalPerformance: str = ""
    position: str = ""
    delayCode: str = ""
    


