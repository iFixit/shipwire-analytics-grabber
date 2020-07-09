RUN_DATE = "RUN_FOR_DATE"
import datetime
from os import environ

import pytz


def get_run_dates():
    mst = pytz.timezone("America/Phoenix")
    now = datetime.datetime.now(tz=mst)

    if RUN_DATE in environ:
        today = datetime.date.fromisoformat(environ[RUN_DATE])
    else:
        today = now.date()

    yesterday = datetime.datetime.combine(
        today - datetime.timedelta(days=1), datetime.time.min
    )
    today = datetime.datetime.combine(
        yesterday + datetime.timedelta(days=1), datetime.time.min
    )
    return (yesterday, today)
