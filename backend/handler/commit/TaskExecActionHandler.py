#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime
from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
import ujson
import calendar
from backend.handler.util.DateUtil import DateUtil
from backend.handler.util.ArrayUtil import ArrayUtil

class TaskExecActionHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._user_group_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_group_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")

    def matchWeekDay(self, weekDay, periodDate):
        weekDayid = 'DUTY_PERIOD_WEEK_' + str(weekDay)
        return (weekDayid in periodDate)

    def matchMonthDay(self, monthDay, periodDate):
        monthDayid = 'DUTY_PERIOD_DATE_' + str(monthDay)
        return (monthDayid in periodDate)

    def shouldPickDuty(self, duty, startofday):
        if duty['timeType'] == Const.DUTY_TIME_TYPE_ROUTINE:
            return True
        elif duty['timeType'] == Const.DUTY_TIME_TYPE_PERIODICAL:
            date = datetime.datetime.fromtimestamp(startofday)
            if duty['periodType'] == Const.DUTY_PERIOD_TYPE_WEEK:
                # 计算startofday 是星期几
                return self.matchWeekDay(date.weekday(), duty['periodDate'])
            elif duty['periodType'] == Const.DUTY_PERIOD_TYPE_MONTH:
                # 计算startofday 是一个月的第几天
                return self.matchMonthDay(date.day, duty['periodDate'])
        elif duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
            if duty['starttime'] <= startofday and duty['endtime'] > startofday:
                return True
        return False

    def getUserGroupDuty(self, userId):
        duties = []
        userGroups = self._user_group_info_coll.find()
        if userGroups:
            for group in userGroups:
                if userId in group['members']:
                    duties = duties + group['duty']
        return duties

    def process_request(self):
        if self._op == 'get_task_exec_info_by_date':
            print 'get task exec info by date!'
            arguments = ujson.loads(self.request.body)
            if 'userid' in arguments:
                userid = arguments['userid']
            else:
                userid = self.current_user
            if 'timeType' in arguments:
                timeType = arguments['timeType']
            else:
                timeType = ''
            if 'startofday' in arguments:
                startofday = arguments['startofday']
            else:
                startofday = DateUtil.get_startof_today()
            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userDuties = user['duty']
                if timeType == Const.DUTY_TIME_TYPE_ALL or timeType == '':
                    groupDuties = self.getUserGroupDuty(user['_id'])
                    if len(groupDuties) > 0:
                        userDuties = ArrayUtil.noDuplicateJoin(userDuties, groupDuties)
                if timeType == Const.DUTY_TIME_TYPE_GROUP:
                    groupDuties = self.getUserGroupDuty(user['_id'])
                    userDuties = groupDuties

                if timeType == '' or timeType == Const.DUTY_TIME_TYPE_ALL or timeType == Const.DUTY_TIME_TYPE_GROUP:
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}}).sort('starttime', 1)
                else:
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}, "timeType": timeType}).sort(
                        'starttime', 1)

            result = []

            for index, duty in enumerate(allUserDuties):
                if not self.shouldPickDuty(duty, startofday):
                    # 如果此职责不需要显示在查询的date的职责列表上的话，直接跳过
                    continue
                dutyId = duty['_id']
                if timeType == Const.DUTY_TIME_TYPE_SPECIFIC:
                    # 对于特定时间的职责，因为是一个日期范围，所以查询时不能带startofday
                    query = {'userid': userid, 'taskid': dutyId}
                else:
                    query = {'userid': userid, 'taskid': dutyId, 'startofday': startofday}
                data = self._task_exec_data_coll.find_one(query)
                if not data:
                    data = {}
                    data['userid'] = userid
                    data['taskid'] = dutyId
                    data['startofday'] = startofday
                    data['realendtime'] = 0
                    data['comment'] = ''
                    data['approve_status'] = Const.TASK_APPROVE_STATUS_NONE
                    data['approve_user'] = ''

                data['starttime'] = duty['starttime']
                data['endtime'] = duty['endtime']
                data['name'] = duty['name']
                data['seq'] = index + 1
                data['descr'] = duty['descr']
                result.append(data)

            self.json_result = result
        elif self._op == 'get_user_task_exec_info_by_daterange':
            print 'get user task exec info by daterange!'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']
            if 'timeType' in arguments:
                timeType = arguments['timeType']
            else:
                timeType = ''
            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userDuties = user['duty']
                groupDuties = self.getUserGroupDuty(user['_id'])
                if len(groupDuties) > 0:
                    userDuties = ArrayUtil.noDuplicateJoin(userDuties, groupDuties)

                if timeType == '':
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}}).sort('starttime', 1)
                else:
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}, "timeType": timeType}).sort(
                        'starttime', 1)

            result = []
            startofday = arguments['startofday']
            endofday = arguments['endofday'] + 3600 * 24 - 1
            dateStart = datetime.datetime.fromtimestamp(startofday)
            dateEnd = datetime.datetime.fromtimestamp(endofday)
            query = {'userid': userid, 'startofday': {'$gte': startofday, '$lt': endofday}}
            taskData = list(self._task_exec_data_coll.find(query))

            for index, duty in enumerate(allUserDuties):
                if duty['timeType'] == Const.DUTY_TIME_TYPE_ROUTINE:
                    dayCount = DateUtil.getWorkDays(dateStart, dateEnd)
                elif duty['timeType'] == Const.DUTY_TIME_TYPE_PERIODICAL:
                    # dayCount = 0
                    # count = (endofday - startofday) / (3600 * 24)
                    # if duty['periodType'] == Const.DUTY_PERIOD_TYPE_WEEK:
                    #     startWeekday = dateStart.weekday()
                    #     for i in range(count):
                    #         weekday = (startWeekday + i) % 7
                    #         if self.matchWeekDay(weekday, duty['periodDate']):
                    #             dayCount += 1
                    # elif duty['periodType'] == Const.DUTY_PERIOD_TYPE_MONTH:
                    #     startMonthday = dateStart.day
                    #     month = dateStart.month
                    #     year = dateStart.year
                    #     dayofMonth = calendar.monthrange(year, month)
                    #     for i in range(count):
                    #         monthday = (startMonthday + i)
                    #         if monthday > dayofMonth:
                    #             monthday = 1
                    #             month += 1
                    #             if month > 12:
                    #                 month = 1
                    #                 year += 1
                    #             dayofMonth = calendar.monthrange(year, month)
                    #         if self.matchMonthDay(monthday, duty['periodDate']):
                    #             dayCount += 1
                    dayCount = DateUtil.getPeriodicalWorkDays(dateStart, dateEnd, duty['periodType'], duty['periodDate'])
                else:
                    if startofday <= duty['endtime'] and endofday >= duty['starttime']:
                        dayCount = 1
                    else:
                        dayCount = 0

                if dayCount > 0:
                    dutyId = duty['_id']
                    finishCount = 0
                    for taskexec in taskData:
                        if taskexec['taskid'] == dutyId:
                            realendtime = taskexec['realendtime']
                            if taskexec['finish_status'] == Const.TASK_STATUS_FINISHED:
                                if duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
                                    taskEndtime = duty['endtime']
                                    if realendtime < taskEndtime + 3600 * 24:
                                        finishCount += 1
                                else:
                                    if realendtime < taskexec['startofday'] + 3600 * 24:
                                        # 只要是当天提交的就可以算完成
                                        finishCount += 1

                    item = {}
                    item['seq'] = index + 1
                    item['userid'] = user['_id']
                    item['username'] = user['name']
                    item['taskid'] = dutyId
                    item['taskname'] = duty['name']

                    item['unfinish_count'] = dayCount - finishCount
                    if item['unfinish_count'] < 0:
                        item['unfinish_count'] = 0
                    result.append(item)

            self.json_result = result
        elif self._op == 'get_one_task_exec_info_by_daterange':
            print 'get one task exec info by daterange!'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']
            taskid = arguments['taskid']
            startofday = arguments['startofday']
            endofday = arguments['endofday'] + 3600 * 24 - 1
            now = DateUtil.get_current_time()
            result = []
            task = self._duty_info_coll.find_one({'_id': taskid})
            query = {'userid': userid, 'taskid': taskid, 'startofday': {'$gte': startofday, '$lt': endofday}}
            taskexecdata = list(self._task_exec_data_coll.find(query))
            if True:
                if task['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
                    item = {}
                    item['starttime'] = task['starttime']
                    item['endtime'] = task['endtime']
                    if len(taskexecdata) > 0:
                        item['realendtime'] = taskexecdata[0]['realendtime']
                        item['comment'] = taskexecdata[0]['comment']
                        item['approve_status'] = taskexecdata[0]['approve_status']
                        item['approve_user'] = taskexecdata[0]['approve_user']
                        item['finish_status'] = taskexecdata[0]['finish_status']
                    else:
                        item['realendtime'] = 0
                        item['comment'] = ''
                        item['approve_status'] = Const.TASK_APPROVE_STATUS_NONE
                        item['approve_user'] = ''
                        if now < task['endtime'] + 3600 * 24:
                            item['finish_status'] = Const.TASK_STATUS_INPROCESS
                        else:
                            item['finish_status'] = Const.TASK_STATUS_UNFINISHED
                    item['timeType'] = task['timeType']
                    item['startofday'] = DateUtil.get_startof_today()
                    result.append(item)
                else:
                    dayCount = (endofday - startofday) / (3600 * 24) + 1
                    for index in range(dayCount):
                        item = {}
                        date = startofday + 3600 * 24 * index
                        theDay = datetime.datetime.fromtimestamp(date)
                        if task['timeType'] == Const.DUTY_TIME_TYPE_ROUTINE and (theDay.weekday() == 5 or theDay.weekday() == 6):
                            continue
                        if task['timeType'] == Const.DUTY_TIME_TYPE_PERIODICAL:
                            if task['periodType'] == Const.DUTY_PERIOD_TYPE_WEEK:
                                dateName = "{:s}{:d}".format(Const.DUTY_PERIOD_WEEK_PREFIX, theDay.weekday())
                            elif task['periodType'] == Const.DUTY_PERIOD_TYPE_MONTH:
                                dateName = "{:s}{:d}".format(Const.DUTY_PERIOD_MONTH_PREFIX, theDay.day)
                            else:
                                dateName = ''
                            if not dateName in task['periodDate']:
                                continue

                        taskexecdata_cursor = 0
                        for dd in taskexecdata:
                            if dd['startofday'] < date:
                                taskexecdata_cursor += 1
                            else:
                                break

                        if taskexecdata_cursor < len(taskexecdata) and date == taskexecdata[taskexecdata_cursor][
                            'startofday']:
                            item['startofday'] = date
                            item['realendtime'] = taskexecdata[taskexecdata_cursor]['realendtime']
                            item['comment'] = taskexecdata[taskexecdata_cursor]['comment']
                            item['approve_status'] = taskexecdata[taskexecdata_cursor]['approve_status']
                            item['approve_user'] = taskexecdata[taskexecdata_cursor]['approve_user']
                            item['finish_status'] = taskexecdata[taskexecdata_cursor]['finish_status']
                            taskexecdata_cursor += 1
                        else:
                            item['startofday'] = date
                            item['realendtime'] = 0
                            item['comment'] = ''
                            item['approve_status'] = Const.TASK_APPROVE_STATUS_NONE
                            item['approve_user'] = ''
                            if now < item['startofday'] + 3600 * 24:
                                item['finish_status'] = Const.TASK_STATUS_INPROCESS
                            else:
                                item['finish_status'] = Const.TASK_STATUS_UNFINISHED
                        item['starttime'] = task['starttime']
                        item['endtime'] = task['endtime']
                        item['timeType'] = task['timeType']
                        result.append(item)

            self.json_result = result
        elif self._op == 'mobile_get_task_exec_info_by_date':
            # 按照timeType进行分组，然后返回
            print 'mobile get task exec info by date!'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']

            if 'timeType' in arguments:
                timeType = arguments['timeType']
            else:
                timeType = ''
            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userDuties = user['duty']
                if timeType == Const.DUTY_TIME_TYPE_ALL or timeType == '':
                    groupDuties = self.getUserGroupDuty(user['_id'])
                    if len(groupDuties) > 0:
                        userDuties = ArrayUtil.noDuplicateJoin(userDuties, groupDuties)
                if timeType == Const.DUTY_TIME_TYPE_GROUP:
                    groupDuties = self.getUserGroupDuty(user['_id'])
                    userDuties = groupDuties

                if timeType == '' or timeType == Const.DUTY_TIME_TYPE_ALL or timeType == Const.DUTY_TIME_TYPE_GROUP:
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}}).sort('starttime', 1)
                else:
                    allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}, "timeType": timeType}).sort(
                        'starttime', 1)

            result = {}
            now = DateUtil.get_current_time()
            startofday = arguments['startofday']
            for index, duty in enumerate(allUserDuties):
                if not self.shouldPickDuty(duty, startofday):
                    # 如果此职责不需要显示在查询的date的职责列表上的话，直接跳过
                    continue
                dutyId = duty['_id']
                dutyTimeType = duty['timeType']
                if timeType == Const.DUTY_TIME_TYPE_SPECIFIC:
                    # 对于特定时间的职责，因为是一个日期范围，所以查询时不能带startofday
                    query = {'userid': userid, 'taskid': dutyId}
                else:
                    query = {'userid': userid, 'taskid': dutyId, 'startofday': startofday}
                data = self._task_exec_data_coll.find_one(query)
                if not data:
                    data = {}
                    data['userid'] = userid
                    data['taskid'] = dutyId
                    data['startofday'] = startofday
                    data['realendtime'] = 0
                    data['comment'] = ''
                    data['approve_status'] = Const.TASK_APPROVE_STATUS_NONE
                    data['approve_user'] = ''
                    if timeType == Const.DUTY_TIME_TYPE_SPECIFIC:
                        if now < duty['endtime'] + 3600 * 24:
                            data['finish_status'] = Const.TASK_STATUS_INPROCESS
                        else:
                            data['finish_status'] = Const.TASK_STATUS_UNFINISHED
                    else:
                        if now < data['startofday'] + 3600 * 24:
                            data['finish_status'] = Const.TASK_STATUS_INPROCESS
                        else:
                            data['finish_status'] = Const.TASK_STATUS_UNFINISHED

                data['starttime'] = duty['starttime']
                data['endtime'] = duty['endtime']
                data['name'] = duty['name']
                data['seq'] = index + 1
                data['descr'] = duty['descr']
                data['timeType'] = duty['timeType']
                if not dutyTimeType in result:
                    result[dutyTimeType] = []
                result[dutyTimeType].append(data)

            self.json_result = result
        elif self._op == 'commit_task_exec_info':
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']
            taskid = arguments['taskid']
            startofday = arguments['startofday']
            now = DateUtil.get_current_time()
            query = {'userid': userid, 'taskid': taskid, 'startofday': startofday}
            item = self._task_exec_data_coll.find_one(query)
            if not item:
                item = {}
                item['taskid'] = taskid
                item['userid'] = userid
                item['startofday'] = startofday
                item['realendtime'] = now
                item['finish_status'] = ''
            if 'finish_status' in arguments:
                if item['finish_status'] != arguments['finish_status']:
                    if arguments['finish_status'] == Const.TASK_STATUS_INPROCESS:
                        self._task_exec_data_coll.remove(query)
                        return
                    elif arguments['finish_status'] == Const.TASK_STATUS_FINISHED:
                        return
                    item['finish_status'] = arguments['finish_status']
            else:
                if arguments['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
                    if item['realendtime'] < arguments['endtime'] + 3600 * 24:
                        item['finish_status'] = Const.TASK_STATUS_FINISHED
                    else:
                        item['finish_status'] = Const.TASK_STATUS_UNFINISHED
                else:
                    if item['realendtime'] < startofday + 3600 * 24:
                        item['finish_status'] = Const.TASK_STATUS_FINISHED
                    else:
                        item['finish_status'] = Const.TASK_STATUS_UNFINISHED

            item['comment'] = arguments["comment"]
            item['approve_status'] = arguments['approve_status']
            item['approve_user'] = arguments['approve_user']
            if 'locationLat' in arguments:
                item['locationLat'] = arguments['locationLat']
            else:
                item['locationLat'] = 0
            if 'locationLng' in arguments:
                item['locationLng'] = arguments['locationLng']
            else:
                item['locationLng'] = 0
            self._task_exec_data_coll.save(item)
            self.json_result = {'status': 0}
        super(TaskExecActionHandler, self).process_request()
