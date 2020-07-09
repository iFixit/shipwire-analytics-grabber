from datetime import datetime, timedelta

import pytest

import dates


def test_missing_var(monkeypatch):
    monkeypatch.delenv("RUN_FOR_DATE", raising=False)

    with pytest.raises(RuntimeError, match=r"RUN_FOR_DATE"):
        dates.get_run_dates()


def test_resolve(monkeypatch):
    monkeypatch.setenv("RUN_FOR_DATE", "2020-07-08")

    yesterday, today = dates.get_run_dates()
    assert today == datetime(2020, 7, 8, 0, 0, 0)
    assert yesterday == datetime(2020, 7, 7, 0, 0, 0)
    assert today.utcoffset() == None
    assert yesterday.utcoffset() == None
