import arrow
from dateutil import tz
from aaLogbook import xmlTranslation, logbookTranslation
from pathlib import Path
from importlib import resources


def test_Arrow():
    dt = arrow.get("2016-10-20T18:15:00")
    print("\n", dt)
    dt2 = arrow.get(dt.datetime, tz.gettz('America/New_York'))
    print(dt2)
    dt3 = dt.replace(tzinfo="America/New_York")
    print(dt3)


def loadXml()->xmlTranslation.LogbookElement:
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
    logbookElement = loadXml()
    logbook = logbookTranslation.buildLogbook(logbookElement)
    logbookTranslation.save_logbookCsv(logbook, savePath)


def test_buildFlightRowDict():
    data = translateParsedXml()
    dataDict = logbookTranslation.buildFlightRowDict(data)
    print(dataDict)


def test_lambda():
    dur = logbookTranslation.Duration(hours=3, minutes=35)
    foo = lambdaFunc()
    print(dur.to_timedelta())
    print(foo(dur))


def lambdaFunc():
    return lambda x: str(x.to_timedelta())
