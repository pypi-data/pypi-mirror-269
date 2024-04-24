import re
from datetime import date, datetime, time, timedelta


def date2grdate(a_date: date) -> str:
    """Transform date object to greek formatted date string"""
    isod = a_date.isoformat()
    year, month, day = isod.split("-")
    return f"{day}/{month}/{year}"


def isodate2gr(iso_date: str) -> str:
    """Transform iso date string to greek formatted date string

    :param date: Iso formatted date string (yyyy-mm-dd)
    :return: Greek formatted date string (dd/mm/yyyy)
    """
    strdate = str(iso_date)
    try:
        year, month, day = strdate.split("-")
        return "%s/%s/%s" % (day, month, year)
    except ValueError:
        return "01/01/1000"


def isodate2yearmonth(isodate: str):
    """2023-01-15 => 2023-01"""
    return isodate[:7]


def grdate2isodate(grdate: str) -> str:
    """Transform Greek date string to iso date string

    :param grdate: Greek Date string
    :return: Iso Date string
    """
    strdate = str(grdate)
    try:
        day, month, year = strdate.split("/")
    except ValueError:
        return "1000-01-01"
    if len(month) > 2 or len(day) > 2 or len(year) != 4:
        return "1000-01-01"
    day = day if len(day) == 2 else "0" + day
    month = month if len(month) == 2 else "0" + month
    return "%s-%s-%s" % (year, month, day)


def grdate2date(grdate: str) -> date:
    """Transform Greek date string to date object"""
    day, month, year = grdate.split("/")
    return date(int(year), int(month), int(day))


def is_greek_date(grdate: str) -> bool:
    return re.match(r"\d{2}\/\d{2}\/\d{4}", grdate, re.I)


def delta_hours(apo: datetime, eos: datetime) -> float:
    """Returns hours between two datetime objects"""
    delta = eos - apo
    return round(delta.seconds / 3600, 1)


def round_half(hours: float) -> float:
    """Ωρες στρογγυλεμένες ανα μισάωρο"""
    return round(hours * 2) / 2


def daynight_hours(dapo: datetime, deos: datetime) -> dict[str, float]:
    """
    Calculate the number of day and night hours between two datetime objects.

    Parameters:
    - dapo: datetime object representing the start datetime
    - deos: datetime object representing the end datetime

    Returns:
    - HOURS object containing the number of day and night hours
    """
    day_start = time(6, 0)  # 6:00 AM
    day_end = time(22, 0)  # 10:00 PM
    dt_day_start = datetime.combine(dapo, day_start)
    dt_day_end = datetime.combine(dapo, day_end)
    dt_next_day_start = dt_day_start + timedelta(days=1)

    # dts: dt_day_start, dte: dt_day_end, ndts: dt_next_day_start
    #
    #       dts            dte       ndts
    # 0     6              22        6                22
    #  -----|---------------|--+-----|----------------|--
    # 1  *-*|               |        |
    # 2  *--|----------*    |        |
    #    *--|---------------|-*      |    Αδύνατο
    # 3     |  *--------*   |        |
    # 4     |            *--|------* |
    # 5     |             *-|--------|--*
    # 6     |               |   *---*|
    # 7     |               |   *----|-------*

    night_hours = 0
    day_hours = 0

    # 1
    if dapo < dt_day_start and deos <= dt_day_start:
        night_hours += delta_hours(dapo, deos)
    # 2
    elif dapo < dt_day_start and dt_day_start <= deos <= dt_day_end:
        night_hours += delta_hours(dapo, dt_day_start)
        day_hours += delta_hours(dt_day_start, deos)
    # 3
    elif dt_day_start <= dapo <= dt_day_end and dt_day_start < deos <= dt_day_end:
        day_hours += delta_hours(dapo, deos)
    # 4
    elif dt_day_start < dapo < dt_day_end and dt_day_end < deos <= dt_next_day_start:
        day_hours += delta_hours(dapo, dt_day_end)
        night_hours += delta_hours(dt_day_end, deos)
    # 5
    elif dt_day_start < dapo < dt_day_end and dt_next_day_start < deos:
        day_hours += delta_hours(dapo, dt_day_end)
        night_hours += delta_hours(dt_day_end, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, deos)
    # 6
    elif (
        dt_day_end <= dapo < dt_next_day_start
        and dt_day_end < deos <= dt_next_day_start
    ):
        night_hours += delta_hours(dapo, dt_next_day_start)
    # 7
    elif dt_day_end <= dapo < dt_next_day_start and dt_next_day_start < deos:
        night_hours += delta_hours(dapo, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, deos)
    else:
        raise ValueError(f"Wrong TimeRange {dapo}-{deos}")

    return {"day_hours": day_hours, "night_hours": night_hours}


def do_overlap(from1: datetime, to1: datetime, from2: datetime, to2: datetime) -> bool:
    """Checks if two time ranges overlap"""
    return from1 < to2 and from2 < to1