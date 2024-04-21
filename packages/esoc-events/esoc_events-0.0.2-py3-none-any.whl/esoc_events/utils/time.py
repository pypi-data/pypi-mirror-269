from datetime import datetime, timedelta


def parse_time(utc: str) -> datetime:
    """
    Args:
        utc (str): "2023-104T12:47:12.000Z" or  "2023-10-04T12:47:12.000Z"

    Returns:
        datetime: the corresponding date
    """
    try:
        date = parse_fdyn_time(utc)
    except ValueError:
        date = parse_utc_time(utc)
        return date
    else:
        return date


def parse_fdyn_time(doy_utc: str) -> datetime:
    """
    Args:
        doy_utc (str): "2023-104T12:47:12.000Z"

    Returns:
        datetime: the corresponding date
    """
    fdyn_format = "%Y-%jT%H:%M:%S.%fZ"
    return datetime.strptime(doy_utc, fdyn_format)


def parse_utc_time(utc_time: str) -> datetime:
    """
    Args:
        utc (str): "2023-10-04T12:47:12.000Z"

    Returns:
        datetime: the corresponding date
    """
    utc_format = "%Y-%m-%dT%H:%M:%S.%fZ"
    return datetime.strptime(utc_time, utc_format)


def format_time(date: datetime) -> str:
    """
    Args:
        date (datetime)

    Returns:
        str: the ISOC representation "2023-104T12:47:12Z"
    """

    return date.isoformat(timespec="seconds") + "Z"


def fdyn_to_iso(doy_utc: str) -> str:
    """
    Args:
        doy_utc (str): "2023-104T12:47:12.000Z"

    Returns:
        str: the ISOC representation "2023-104T12:47:12Z"
    """
    return format_time(parse_time(doy_utc))


def get_timedelta(milliseconds: str) -> timedelta:
    """The time delta object corresponding to the milliseconds string

    Args:
        milliseconds (str): duration expressed in milliseconds

    Returns:
        timedelta: the corresponding time delta
    """
    return timedelta(milliseconds=int(milliseconds))
