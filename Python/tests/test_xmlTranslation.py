"""
"""

from aaLogbook import xmlTranslation
from aaLogbook.models.xmlElementModel import LogbookElement
from utilities import timedelta_util
from pathlib import Path
from importlib import resources
import json
import dataclasses
from dataclasses_json import dataclass_json
from utilities import csv_util


def loadXml()->LogbookElement:
    xmlPath = pathToXmlInput()
    parsedXML = xmlTranslation.parseXML(xmlPath)
    return parsedXML


def pathToDataDirectory()->Path:
    with resources.path('tests', 'resources') as filePath:
        return filePath


def pathToXmlInput()->Path:
    xmlPath = pathToDataDirectory() / Path('myCrystalReportViewer.xml')
    return xmlPath


def test_saveRawJson():
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path('raw.json')
    xmlTranslation.saveRawJson(xmlPath, savePath)


def test_saveRawFlatJson():
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path('raw_flat.json')
    xmlTranslation.saveRawFlatJson(xmlPath, savePath)


def test_saveRawCsv():
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path('raw.csv')
    xmlTranslation.saveRawCsv(xmlPath, savePath)


def test_rawFlat():
    xmlPath = pathToXmlInput()
    logbookElement = xmlTranslation.parseXML(xmlPath)
    print(logbookElement.uuid, type(logbookElement.uuid))


def test_printParsedXmlToStdOut():
    print(loadXml().to_json(indent=2))  # pylint: disable=E1101
