from datetime import date


def date2grdate(a_date: date) -> str:
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
    return isodate[:7]
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
    day, month, year = grdate.split("/")
    return date(int(year), int(month), int(day))
