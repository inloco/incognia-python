import datetime as dt


def total_milliseconds_since_epoch(t: dt.datetime) -> int:
    return int((t - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)
