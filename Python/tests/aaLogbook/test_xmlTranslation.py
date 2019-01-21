"""
"""

from aaLogbook import xmlTranslation
from pathlib import Path
from datetime import timedelta
import json
import dataclasses
from dataclasses_json import dataclass_json
 

def test_assertTrue():
    assert True

def test_loadXml():
    path=Path('Python/tests/resources/myCrystalReportViewer.xml')
    parsedXML = xmlTranslation.parseXML(path)
    # pylint: disable=E1101
    print(parsedXML.to_json(indent=2))
    
def test_stringTo_timedelta():
    string1 = '23.34'
    td1 = xmlTranslation.parse_HHdotMM_ToTimeDelta(string1)
    assert(td1==timedelta(hours=23,minutes=34))
    
# def test_timedeltaToIsoString():
#     td1 = timedelta(hours=23,minutes=34)
#     tdString = xmlTranslation.timeDeltaToIsoString(td1)
#     assert(tdString=="PT23H34M0S")
