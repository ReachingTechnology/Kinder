# -*- coding: utf-8 -*-
#

from datetime import date
from datetime import datetime
from time import strptime
import time


class DateUtil(object):

    @classmethod
    def get_current_day(cls):
        return datetime.date.today()

    @classmethod
    def get_current_time(cls):
        return time.mktime(datetime.now().timetuple())

    @classmethod
    def get_startof_today(cls):
        now = datetime.date()
        today = datetime(now.year, now.month, now.day)
        return time.mktime(today.timetuple())

    @classmethod
    def convert_str_to_date(cls, dateStr):
        return date(*strptime(dateStr, "%Y-%m-%d")[0:3])

    @classmethod
    def convert_datetime_to_date(cls, dateTimeStr):
        return date(*strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S')[0:3])

    @classmethod
    def convert_str_to_datetime(cls, dateTimeStr):
        return datetime(*strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S')[0:6])