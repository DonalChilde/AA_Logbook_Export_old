from datetime import timedelta
from dataclasses import dataclass


def parse_isoformatDuration(durationString: str) -> timedelta:
    pass


def parse_HHMMSS(durationString: str, separator: str = ":") -> timedelta:
    pass


def parse_HHdotMM_To_timedelta(durationString: str, separator: str = ".") -> timedelta:
    """
    parses a string in the format "34.23", assuming HH.MM
    """
    hours, minutes = durationString.split(separator)
    hours, minutes = map(int, (hours, minutes))  # type: ignore
    return timedelta(hours=hours, minutes=minutes)  # type: ignore


@dataclass
class TimeDeltaSplit:
    days: int = 0
    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    microseconds: int = 0


def timedelta_split(timeDelta: timedelta) -> TimeDeltaSplit:
    int_seconds = 0
    if timeDelta.days:
        int_seconds = int_seconds + (abs(timeDelta.days) * 86400)
    if timeDelta.seconds:
        int_seconds = int_seconds + timeDelta.seconds
    minutes, seconds = divmod(int_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    microseconds = timeDelta.microseconds
    return TimeDeltaSplit(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )


def timeDelta_TO_HHMMSS(timeDelta: timedelta, separator: str = ":"):
    timeSplit = timedelta_split(timeDelta)
    totalHours = (timeSplit.days * 24) + timeSplit.hours
    if timeSplit.microseconds:
        decimalSecondsString = f".{timeSplit.microseconds:06d}"
    else:
        decimalSecondsString = ""
    return f"{totalHours}{separator}{timeSplit.minutes}{separator}{timeSplit.seconds}{decimalSecondsString}"


def timedelta_To_isoformat(timeDelta: timedelta, strict=True) -> str:
    """
    if strict then limit output fields to PddDThhHmmMss.sS # Not implemeted
    """
    # int_seconds = 0
    # if timeDelta.days:
    #     int_seconds = int_seconds + (abs(timeDelta.days)*86400)
    # if timeDelta.seconds:
    #     int_seconds = int_seconds + timeDelta.seconds
    # minutes, seconds = divmod(int_seconds, 60)
    # hours, minutes = divmod(minutes, 60)
    # days, hours = divmod(hours, 24)
    # microseconds = timeDelta.microseconds
    timeSplit = timedelta_split(timeDelta)
    daystext = hourstext = minutestext = secondstext = microtext = ""
    if timeSplit.days:
        daystext = f"{timeSplit.days}D"
    if timeSplit.hours:
        hourstext = f"{timeSplit.hours}H"
    if timeSplit.minutes:
        minutestext = f"{timeSplit.minutes}M"
    if timeSplit.microseconds:
        if not timeSplit.seconds:
            timeSplit.seconds = 0
        microtext = f".{timeSplit.microseconds:06d}"
    if timeSplit.seconds or timeSplit.microseconds:
        secondstext = f"{timeSplit.seconds}{microtext}S"
    if not (
        timeSplit.hours
        or timeSplit.minutes
        or timeSplit.seconds
        or timeSplit.microseconds
    ):
        secondstext = f"{timeSplit.seconds}S"
    isoString = f"P{daystext}T{hourstext}{minutestext}{secondstext}"
    return isoString
