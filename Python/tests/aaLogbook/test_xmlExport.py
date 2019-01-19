"""
"""

from aaLogbook import xmlExport
from pathlib import Path
from datetime import timedelta
import json
import dataclasses
from dataclasses_json import dataclass_json
 

def test_assertTrue():
    assert True

def test_loadXml():
    path=Path('Python/tests/resources/myCrystalReportViewer.xml')
    parsedXML = xmlExport.parseXML(path)
    # pylint: disable=E1101
    print(parsedXML.to_json(indent=2))
    
    

