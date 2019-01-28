"""
"""

from aaLogbook import xmlTranslation
from utilities import timedelta_util
from pathlib import Path
from datetime import timedelta
from importlib import resources
# from timeDelta import parse_HHdotMM_To_timedelta
import json
import dataclasses
from dataclasses_json import dataclass_json
import arrow
from dateutil import tz
from utilities import csv_util


def test_assertTrue():
    assert True


def loadXml():
    xmlPath = pathToDataDirectory() /Path('myCrystalReportViewer.xml')
    parsedXML = xmlTranslation.parseXML(xmlPath)
    return parsedXML

def pathToDataDirectory()->Path:
    with resources.path('tests', 'resources') as filePath:
        return filePath

def test_saveRawJson():
    xmlPath = pathToDataDirectory() /Path('myCrystalReportViewer.xml')
    savePath = pathToDataDirectory() / Path('raw.json')
    xmlTranslation.saveRawJson(xmlPath,savePath)

def test_saveRawFlatJson():
    xmlPath = pathToDataDirectory() /Path('myCrystalReportViewer.xml')
    savePath = pathToDataDirectory() / Path('raw_flat.json')
    xmlTranslation.saveRawFlatJson(xmlPath,savePath)

def test_saveRawCsv():
    xmlPath = pathToDataDirectory() /Path('myCrystalReportViewer.xml')
    savePath = pathToDataDirectory() / Path('raw.csv')
    xmlTranslation.saveRawCsv(xmlPath,savePath)

def test_rawFlat():
    xmlPath = pathToDataDirectory() /Path('myCrystalReportViewer.xml')
    logbookElement = xmlTranslation.parseXML(xmlPath)
    print(logbookElement.uuid,type(logbookElement.uuid))


def test_printParsedXmlToStdOut():
    print(loadXml().to_json(indent=2))

