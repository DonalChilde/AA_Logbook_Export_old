import arrow
from dateutil import tz
from aaLogbook import xmlTranslation, logbookTranslation
from aaLogbook.models.xmlElementModel import LogbookElement
from aaLogbook.models.logbookTranslationModel import Duration
from pathlib import Path
from importlib import resources
from time import perf_counter


def test_Arrow():
    dt = arrow.get("2016-10-20T18:15:00")
    print("\n", dt)
    dt2 = arrow.get(dt.datetime, tz.gettz('America/New_York'))
    print(dt2)
    dt3 = dt.replace(tzinfo="America/New_York")
    print(dt3)


def loadXml()->LogbookElement:
    xmlPath = pathToXmlInput()
    parsedXML = xmlTranslation.parseXML(xmlPath)
    return parsedXML


def pathToXmlInput()->Path:
    xmlPath = pathToDataDirectory() / Path('myCrystalReportViewer.xml')
    return xmlPath


def pathToDataDirectory()->Path:
    with resources.path('tests', 'resources') as filePath:
        return filePath


def translateParsedXml():
    parsed = loadXml()
    translated = logbookTranslation.buildLogbook(parsed)
    return translated


def test_translatedLogToStdOut():
    print(translateParsedXml())


def test_saveLogbookJson():
    savePath = pathToDataDirectory() / Path('translated_log.json')
    logbookElement = loadXml()
    logbookTranslation.save_logbookJson(logbookElement, savePath)

def test_saveLogbookCsv():
    savePath = pathToDataDirectory() / Path('translated_log.csv')
    startTime = perf_counter()
    logbookElement = loadXml()
    xmlParseTime = perf_counter()
    logbook = logbookTranslation.buildLogbook(logbookElement)
    logbookTranslationTime = perf_counter()
    logbookTranslation.save_logbookCsv(logbook, savePath)
    saveFileTime = perf_counter()
    print(f"Time to parse xml: {xmlParseTime-startTime}")
    print(f"Time to translate parsed xml: {logbookTranslationTime-xmlParseTime}")
    print(f"Time to save file: {saveFileTime-logbookTranslationTime}")
    print(f"Total Time: {saveFileTime-startTime}")


def test_buildFlightRowDict():
    data = translateParsedXml()
    dataDict = logbookTranslation.buildFlightRowDict(data)
    print(dataDict)


def test_lambda():
    dur = Duration(hours=3, minutes=35)
    foo = lambdaFunc()
    print(dur.to_timedelta())
    print(foo(dur))


def lambdaFunc():
    return lambda x: str(x.to_timedelta())
