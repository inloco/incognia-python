import datetime as dt


def has_timezone(d: dt.datetime) -> bool:
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None
