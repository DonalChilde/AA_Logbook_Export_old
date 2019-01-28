from utilities.timedelta_util import timedelta_To_isoformat,parse_HHdotMM_To_timedelta
from datetime import timedelta

#days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0

def test_TimeDelta_toiso_1():
    td = timedelta(hours=100,minutes=5,microseconds=5)
    assert(timedelta_To_isoformat(td)=="P4DT4H5M0.000005S")

def test_TimeDelta_toiso_2():
    td = timedelta(days=100,hours=5,microseconds=5)
    assert(timedelta_To_isoformat(td)=="P100DT5H0.000005S")

def test_TimeDelta_toiso_3():
    td = timedelta(days=0,hours=0,microseconds=5)
    assert(timedelta_To_isoformat(td)=="PT0.000005S")

def test_TimeDelta_toiso_4():
    td = timedelta()
    assert(timedelta_To_isoformat(td)=="PT0S")

def test_TimeDelta_toiso_5():
    td = timedelta(seconds=345)
    assert(timedelta_To_isoformat(td)=="PT5M45S")

def test_stringTo_timedelta():
    string1 = '23.34'
    td1 = parse_HHdotMM_To_timedelta(string1)
    assert(td1 == timedelta(hours=23, minutes=34))
