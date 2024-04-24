# -*- coding: utf-8 -*-
import pytz
from datetime import datetime
from enum import Enum

DEFAULT_DATE_PATTERN = "%Y-%m-%d"
DEFAULT_DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"


class DateTimeUnitType(Enum):
    days = "days"
    hours = "hours"
    minutes = "minutes"
    seconds = "seconds"

    def get_divid_numbers(self):
        return {
            self.seconds: 1,
            self.minutes: 60,
            self.hours: 60 * 60,
            self.days: 60 * 60 * 24
        }[self]


class DateTimeUtils(object):

    def __init__(self, timezone):
        self.timezone = pytz.timezone(timezone)

    def get_now(self):
        return datetime.now(self.timezone)

    def get_iso_now(self, microsecond=None):
        """microsecond (0-999999)"""
        if isinstance(microsecond, int) and  microsecond >= 0:
            return self.get_now().replace(microsecond=microsecond).isoformat()  # remove micro second
        return self.get_now().isoformat()

    def get_strnow(self, pattern=DEFAULT_DATETIME_PATTERN):
        return self.get_now().strftime(pattern)

    def str_to_date(self, str_date, pattern=DEFAULT_DATETIME_PATTERN):
        date_time = datetime.strptime(str_date, pattern)
        return self.timezone.localize(date_time)

    def date_to_str(self, date_time, pattern=DEFAULT_DATETIME_PATTERN):
        return str(date_time.strftime(pattern))

    def utc_to_localize(self, date_time):
        return date_time.replace(tzinfo=pytz.utc).astimezone(self.timezone)

    def to_localize(self, date_time):
        return self.timezone.localize(date_time)

    def minus(self, date1, date2, unit=DateTimeUnitType.seconds):
        date_time = date1 - date2 if date1 > date2 else date2 - date1
        seconds = date_time.total_seconds()
        if not unit:
            return seconds
        divid = unit.get_divid_numbers()
        return seconds // divid
