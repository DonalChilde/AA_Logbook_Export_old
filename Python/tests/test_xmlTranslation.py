"""
"""

from aaLogbook import xmlTranslation, logbookDataClass
from utilities import timedelta_util
from pathlib import Path
from datetime import timedelta
# from timeDelta import parse_HHdotMM_To_timedelta
import json
import dataclasses
from dataclasses_json import dataclass_json
import arrow
from dateutil import tz
from utilities import csvUtils


def test_assertTrue():
    assert True

# def test_loadXml():
#     path=Path('Python/tests/resources/myCrystalReportViewer.xml')
#     parsedXML = xmlTranslation.parseXML(path)
#     # pylint: disable=E1101
#     print(parsedXML.to_json(indent=2))


def loadXml():
    path = Path('Python/tests/resources/myCrystalReportViewer.xml')
    parsedXML = xmlTranslation.parseXML(path)
    return parsedXML


def translateParsedXml():
    parsed = loadXml()
    translated = logbookDataClass.buildLogbook(parsed)
    return translated


def test_exportXmlToCsvFile():
    translatedData = loadXml()
    outPath = Path("Python/tests/resources/elementsCsv.csv")
    flightRows = xmlTranslation.buildFlightRows(translatedData)
    fieldList = ('aaNumber', 'year', 'monthYear', 'sequenceInfo', 'uuid', 'flightNumber', 'departureStation', 'outDateTime', 'arrivalStation', 'inDateTime', 'fly', 'legGreater',
                 'actualBlock', 'groundTime', 'overnightDuration', 'eqModel', 'eqNumber', 'eqType', 'eqCode', 'fuelPerformance', 'departurePerformance', 'arrivalPerformance', 'position', 'delayCode')
    csvUtils.writeDictToCsv(outPath, flightRows, fieldList)


def test_saveTranslatedToFile():
    translatedData = translateParsedXml()
    outPath = Path("Python/tests/resources/translatedLogbook.json")
    with open(outPath, 'w') as outFile:
        data = translatedData.to_json()
        jsonData = json.loads(data)
        json.dump(jsonData, outFile, indent=2)
    # print(translateParsedXml().to_json(indent=2))


def test_printParsedXmlToStdOut():
    print(loadXml().to_json(indent=2))


def test_stringTo_timedelta():
    string1 = '23.34'
    td1 = timedelta_util.parse_HHdotMM_To_timedelta(string1)
    assert(td1 == timedelta(hours=23, minutes=34))


def test_Arrow():
    dt = arrow.get("2016-10-20T18:15:00")
    print("\n", dt)
    dt2 = arrow.get(dt.datetime, tz.gettz('America/New_York'))
    print(dt2)
    dt3 = dt.replace(tzinfo="America/New_York")
    print(dt3)


# def test_timedeltaToIsoString():
#     td1 = timedelta(hours=23,minutes=34)
#     tdString = xmlTranslation.timeDeltaToIsoString(td1)
#     assert(tdString=="PT23H34M0S")
