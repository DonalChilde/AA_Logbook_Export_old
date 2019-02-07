from dataclasses import dataclass, field, asdict as dc_asdict
from dataclasses_json import dataclass_json
import uuid


@dataclass
class FlightRow:
    aaNumber: str
    year: str
    monthYear: str
    sequenceInfo: str
    uuid: str
    flightNumber: str
    departureStation: str
    outDateTime: str
    arrivalStation: str
    inDateTime: str
    fly: str
    legGreater: str
    actualBlock: str
    groundTime: str
    overnightDuration: str
    eqModel: str
    eqNumber: str
    eqType: str
    eqCode: str
    fuelPerformance: str
    departurePerformance: str
    arrivalPerformance: str
    position: str
    delayCode: str


@dataclass_json
@dataclass
class LogbookElement:
    uuid: str = ""
    aaNumber: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    years: list = field(default_factory=list)

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())


@dataclass_json
@dataclass
class YearElement:
    uuid: str = ""
    year: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    months: list = field(default_factory=list)

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())


@dataclass_json
@dataclass
class MonthElement:
    uuid: str = ""
    monthYear: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    trips: list = field(default_factory=list)

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())


@dataclass_json
@dataclass
class TripElement:
    uuid: str = ""
    sequenceInfo: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    dutyPeriods: list = field(default_factory=list)

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())


@dataclass_json
@dataclass
class DutyPeriodElement:
    uuid: str = ""
    sumOfActualBlock: str = ""
    sumOfLegGreater: str = ""
    sumOfFly: str = ""
    flights: list = field(default_factory=list)

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())


@dataclass_json
@dataclass
class FlightElement:
    uuid: str = ""
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

    def __post_init__(self):
        if self.uuid == "":
            self.uuid = str(uuid.uuid4())
