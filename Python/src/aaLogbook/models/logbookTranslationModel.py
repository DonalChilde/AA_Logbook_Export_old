from __future__ import annotations
from dataclasses import dataclass, field, asdict as dc_asdict
from dataclasses_json import dataclass_json, DataClassJsonMixin
from datetime import timedelta
from typing import List
import uuid

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
    dutyPeriodNumber: str = ''
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
    years: List['Year'] = field(default_factory=list)


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