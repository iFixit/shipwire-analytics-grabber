from datetime import datetime, timedelta

import pytest

import dates


def test_missing_var(monkeypatch):
    monkeypatch.delenv("RUN_FOR_DATE", raising=False)

    with pytest.raises(RuntimeError, match=r"RUN_FOR_DATE"):
        dates.get_run_dates()


def test_resolve(monkeypatch):
    monkeypatch.setenv("RUN_FOR_DATE", "2020-07-08")

    start, end = dates.get_run_dates()
    assert start == datetime(2020, 7, 8, 0, 0, 0)
    assert end == datetime(2020, 7, 9, 0, 0, 0)
    assert start.utcoffset() == None
    assert end.utcoffset() == None
