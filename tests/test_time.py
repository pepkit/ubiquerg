"""Tests for ubiquerg.time module."""

import datetime

import pytest

from ubiquerg import parse_timedelta


class TestParseTimedelta:
    def test_basic_hms(self):
        assert parse_timedelta("0:01:30") == datetime.timedelta(minutes=1, seconds=30)

    def test_zero(self):
        assert parse_timedelta("0:00:00") == datetime.timedelta(0)

    def test_fractional_seconds(self):
        assert parse_timedelta("0:00:45.50") == datetime.timedelta(seconds=45.5)

    def test_large_hours(self):
        assert parse_timedelta("12:30:15") == datetime.timedelta(hours=12, minutes=30, seconds=15)

    def test_one_day(self):
        assert parse_timedelta("1 day, 2:30:00") == datetime.timedelta(days=1, hours=2, minutes=30)

    def test_multiple_days(self):
        assert parse_timedelta("3 days, 5:15:30") == datetime.timedelta(
            days=3, hours=5, minutes=15, seconds=30
        )

    def test_strips_whitespace(self):
        assert parse_timedelta("  0:05:00  ") == datetime.timedelta(minutes=5)

    def test_one_hour_exact(self):
        assert parse_timedelta("1:00:00") == datetime.timedelta(hours=1)

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            parse_timedelta("not-a-time")

    def test_missing_seconds_raises(self):
        with pytest.raises(ValueError):
            parse_timedelta("1:30")
