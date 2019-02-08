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


def loadXml() -> LogbookElement:
    xmlPath = pathToXmlInput()
    parseContext: dict = {}
    parsedXML = xmlTranslation.parseXML(xmlPath, parseContext)
    return parsedXML


def pathToDataDirectory() -> Path:
    with resources.path("tests", "resources") as filePath:
        return filePath


def pathToXmlInput() -> Path:
    xmlPath = pathToDataDirectory() / Path("myCrystalReportViewer.xml")
    return xmlPath


def test_saveRawJson():
    parseContext: dict = {}
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path("raw.json")
    xmlTranslation.saveRawJson(xmlPath, savePath, parseContext)


def test_saveRawFlatJson():
    parseContext: dict = {}
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path("raw_flat.json")
    xmlTranslation.saveRawFlatJson(xmlPath, savePath, parseContext)


def test_saveRawCsv():
    parseContext: dict = {}
    xmlPath = pathToXmlInput()
    savePath = pathToDataDirectory() / Path("raw.csv")
    xmlTranslation.saveRawCsv(xmlPath, savePath, parseContext)


def test_rawFlat():
    parseContext: dict = {}
    xmlPath = pathToXmlInput()
    logbookElement = xmlTranslation.parseXML(xmlPath, parseContext)
    print(logbookElement.uuid, type(logbookElement.uuid))


def test_printParsedXmlToStdOut():
    print(loadXml().to_json(indent=2))  # pylint: disable=no-member
