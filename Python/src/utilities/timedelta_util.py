
from datetime import timedelta

def parse_isoformatDuration(durationString: str)-> timedelta:
    pass


def parse_HHMMSS(durationString: str, separator: str = ":")-> timedelta:
    pass


def parse_HHdotMM_To_timedelta(durationString: str, separator:str = ".")-> timedelta:
    """
    parses a string in the format "34.23", assuming HH.MM
    """
    hours, minutes = durationString.split(separator)
    hours, minutes = map(int, (hours, minutes))# type: ignore
    return timedelta(hours=hours, minutes=minutes)# type: ignore


def timedelta_To_isoformat(timeDelta: timedelta, strict=True)->str:
    """
    if strict then limit output fields to PddDThhHmmMss.sS # Not implemeted
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
