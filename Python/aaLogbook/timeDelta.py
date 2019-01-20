
from datetime import timedelta


# class TimeDelta(timedelta):
#     # def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
#     #     super().__new__(cls, days=days, seconds=seconds, microseconds=microseconds,
#     #                     milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)
#     # def __new__(cls, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
#     #     return super(TimeDelta,cls).__new__(cls, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0)

#     @classmethod
#     def fromisoformat(cls, durationString: str):  # pylint: disable=E0602
#         pass

#     def isoformat(self, strict=True)->str:
#         """
#         if strict then limit output fields to DDHHMMSS.S # Not implemeted
#         """
#         int_seconds = 0
#         if self.days:
#             int_seconds = int_seconds + (abs(self.days)*86400)
#         if self.seconds:
#             int_seconds = int_seconds + self.seconds
#         minutes, seconds = divmod(int_seconds, 60)
#         hours, minutes = divmod(minutes, 60)
#         days, hours = divmod(hours, 24)
#         microseconds = self.microseconds
#         daystext = hourstext = minutestext = secondstext = microtext = ""
#         if days:
#             daystext = f"{days}D"
#         if hours:
#             hourstext = f"{hours}H"
#         if minutes:
#             minutestext = f"{minutes}M"
#         if microseconds:
#             if not seconds:
#                 seconds = 0
#             microtext = f".{microseconds:06d}"
#         if seconds or microseconds:
#             secondstext = f"{seconds}{microtext}S"
#         if not (hours or minutes or seconds or microseconds):
#             secondstext = f"{seconds}S"
#         isoString = f"P{daystext}T{hourstext}{minutestext}{secondstext}"
#         return isoString

#     @classmethod
#     def parse_HHMMSS(cls, durationString: str, separator: str = ":"):
#         pass

#     @classmethod
#     def parse_HHdotMM_ToTimeDelta(cls, durationString):
#         hours, minutes = durationString.split('.')
#         hours, minutes = map(int, (hours, minutes))
#         return TimeDelta(hours=hours, minutes=minutes)


def parse_isoformatDuration(durationString: str)-> timedelta:
    pass


def parse_HHMMSS(durationString: str, separator: str = ":")-> timedelta:
    pass


def parse_HHdotMM_ToTimeDelta(durationString: str, separator:str = ".")-> timedelta:
    """
    parses a string in the format "34.23", assuming HH.MM
    """
    hours, minutes = durationString.split(separator)
    hours, minutes = map(int, (hours, minutes))# type: ignore
    return timedelta(hours=hours, minutes=minutes)# type: ignore


def timedelta_To_isoformat(timeDelta: timedelta, strict=True)->str:
    """
    if strict then limit output fields to DDHHMMSS.S # Not implemeted
    """
    int_seconds = 0
    if timeDelta.days:
        int_seconds = int_seconds + (abs(timeDelta.days)*86400)
    if timeDelta.seconds:
        int_seconds = int_seconds + timeDelta.seconds
    minutes, seconds = divmod(int_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    microseconds = timeDelta.microseconds
    daystext = hourstext = minutestext = secondstext = microtext = ""
    if days:
        daystext = f"{days}D"
    if hours:
        hourstext = f"{hours}H"
    if minutes:
        minutestext = f"{minutes}M"
    if microseconds:
        if not seconds:
            seconds = 0
        microtext = f".{microseconds:06d}"
    if seconds or microseconds:
        secondstext = f"{seconds}{microtext}S"
    if not (hours or minutes or seconds or microseconds):
        secondstext = f"{seconds}S"
    isoString = f"P{daystext}T{hourstext}{minutestext}{secondstext}"
    return isoString
