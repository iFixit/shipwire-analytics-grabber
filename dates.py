RUN_DATE = "RUN_FOR_DATE"
import datetime
from os import environ


def get_run_dates():
    if RUN_DATE not in environ:
        raise RuntimeError("Expected variable {} in environment".format(RUN_DATE))
    today = datetime.date.fromisoformat(environ[RUN_DATE])

    start_time = datetime.datetime.combine(today, datetime.time.min)
    end_time = datetime.datetime.combine(
        start_time + datetime.timedelta(days=1), datetime.time.min
    )

    return (start_time, end_time)
