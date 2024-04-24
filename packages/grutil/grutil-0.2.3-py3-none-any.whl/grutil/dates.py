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


def delta_hours(dfrom: datetime, dto: datetime) -> float:
    """Returns hours between two datetime objects"""
    delta = dto - dfrom
    return round(delta.seconds / 3600, 1)


def round_half(hours: float) -> float:
    """Hours rounded to nearest half hour"""
    return round(hours * 2) / 2


def daynight_hours(dfrom: datetime, dto: datetime) -> dict[str, float]:
    """
    Calculate the number of day and night hours between two datetime objects.

    Parameters:
    - dfrom: datetime object representing the start datetime
    - dto: datetime object representing the end datetime

    Returns:
    - HOURS object containing the number of day and night hours
    """
    day_start = time(6, 0)  # 6:00 AM
    day_end = time(22, 0)  # 10:00 PM
    dt_day_start = datetime.combine(dfrom, day_start)
    dt_day_end = datetime.combine(dfrom, day_end)
    dt_next_day_start = dt_day_start + timedelta(days=1)

    # dts: dt_day_start, dte: dt_day_end, ndts: dt_next_day_start
    #
    #       dts            dte       ndts
    # 0     6              22        6                22
    #  -----|---------------|--+-----|----------------|--
    # 1  *-*|               |        |
    # 2  *--|----------*    |        |
    #    *--|---------------|-*      |    impossible
    # 3     |  *--------*   |        |
    # 4     |            *--|------* |
    # 5     |             *-|--------|--*
    # 6     |               |   *---*|
    # 7     |               |   *----|-------*

    night_hours = 0
    day_hours = 0

    # 1
    if dfrom < dt_day_start and dto <= dt_day_start:
        night_hours += delta_hours(dfrom, dto)
    # 2
    elif dfrom < dt_day_start and dt_day_start <= dto <= dt_day_end:
        night_hours += delta_hours(dfrom, dt_day_start)
        day_hours += delta_hours(dt_day_start, dto)
    # 3
    elif dt_day_start <= dfrom <= dt_day_end and dt_day_start < dto <= dt_day_end:
        day_hours += delta_hours(dfrom, dto)
    # 4
    elif dt_day_start < dfrom < dt_day_end and dt_day_end < dto <= dt_next_day_start:
        day_hours += delta_hours(dfrom, dt_day_end)
        night_hours += delta_hours(dt_day_end, dto)
    # 5
    elif dt_day_start < dfrom < dt_day_end and dt_next_day_start < dto:
        day_hours += delta_hours(dfrom, dt_day_end)
        night_hours += delta_hours(dt_day_end, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, dto)
    # 6
    elif (
        dt_day_end <= dfrom < dt_next_day_start
        and dt_day_end < dto <= dt_next_day_start
    ):
        night_hours += delta_hours(dfrom, dt_next_day_start)
    # 7
    elif dt_day_end <= dfrom < dt_next_day_start and dt_next_day_start < dto:
        night_hours += delta_hours(dfrom, dt_next_day_start)
        day_hours += delta_hours(dt_next_day_start, dto)
    else:
        raise ValueError(f"Wrong TimeRange {dfrom}-{dto}")

    return {"day_hours": day_hours, "night_hours": night_hours}


def do_overlap(from1: datetime, to1: datetime, from2: datetime, to2: datetime) -> bool:
    """Checks if two time ranges overlap"""
    return from1 < to2 and from2 < to1


def iso2dtime(isodatetime: str) -> datetime:
    return datetime.fromisoformat(isodatetime)


def time_range(trange: str) -> tuple[datetime, datetime]:
    """
    2024-01-01T08:00T16:00 -> 2024-01-01T08:00, 2024-01-01T16:00
    """
    dat, tfrom, tto = trange.split("T")
    datefrom = date.fromisoformat(dat)
    dateto = date.fromisoformat(dat)
    timefrom = time.fromisoformat(tfrom)
    timeto = time.fromisoformat(tto)
    if timefrom > timeto:
        dateto += timedelta(days=1)
    dfrom = datetime.combine(datefrom, timefrom)
    dto = datetime.combine(dateto, timeto)
    return dfrom, dto
