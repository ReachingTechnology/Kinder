# -*- coding: utf-8 -*-
#
import datetime
from time import strptime
import time
import workdays
from backend.common.consts import Const

class DateUtil(object):

    holidayByYear = []

    @classmethod
    def get_current_day(cls):
        return datetime.date.today()

    @classmethod
    def get_current_time(cls):
        return int(time.mktime(datetime.datetime.now().timetuple()))

    @classmethod
    def get_startof_today(cls):
        now = datetime.date.today()
        today = datetime.datetime(now.year, now.month, now.day)
        return int(time.mktime(today.timetuple()))

    @classmethod
    def convert_str_to_date(cls, dateStr):
        return datetime.date(*strptime(dateStr, "%Y-%m-%d")[0:3])

    @classmethod
    def convert_datetime_to_date(cls, dateTimeStr):
        return datetime.date(*strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S')[0:3])

    @classmethod
    def convert_str_to_datetime(cls, dateTimeStr):
        return datetime(*strptime(dateTimeStr, '%Y-%m-%d %H:%M:%S')[0:6])

    @classmethod
    def getWorkDays(cls, startDate, endDate):
        return workdays.networkdays(startDate, endDate)

    @classmethod
    def getPeriodicalWorkDays(cls, startDate, endDate, periodType, periodDate):
        allDays = (endDate - startDate).days + 1
        dayCount = 0
        for i in range(allDays):
            tempdate = startDate + datetime.timedelta(days=i)
            if periodType == Const.DUTY_PERIOD_TYPE_WEEK:
                dateName = "{:s}{:d}".format(Const.DUTY_PERIOD_WEEK_PREFIX, tempdate.weekday())
            elif periodType == Const.DUTY_PERIOD_TYPE_MONTH:
                dateName = "{:s}{:d}".format(Const.DUTY_PERIOD_MONTH_PREFIX, tempdate.day)
            else:
                dateName = ''
            if dateName in periodDate:
                dayCount += 1
        return dayCount

    @classmethod
    def isTodayPeriodicalWorkDays(cls, periodType, periodDate):
        today = DateUtil.get_current_day()
        if periodType == Const.DUTY_PERIOD_TYPE_WEEK:
            weekday = today.weekday()
            name = '{:s}{:d}'.format(Const.DUTY_PERIOD_WEEK_PREFIX, weekday)
            if name in periodDate:
                return True
        elif periodType == Const.DUTY_PERIOD_TYPE_MONTH:
            monthday = today.day
            name = '{:s}{:d}'.format(Const.DUTY_PERIOD_MONTH_PREFIX, monthday)
            if name in periodDate:
                return True
        return False