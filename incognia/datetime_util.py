import datetime as dt


def total_milliseconds_since_epoch(t: dt.datetime) -> int:
    return int((t - dt.datetime.fromtimestamp(0, dt.timezone.utc)).total_seconds() * 1000.0)


def has_timezone(d: dt.datetime) -> bool:
    return d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None
