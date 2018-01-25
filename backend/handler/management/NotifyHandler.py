#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime
from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
import ujson
import calendar
import time
from backend.handler.util.ArrayUtil import ArrayUtil
from backend.handler.util.Util import Util

class NotifyHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")

    def getRoleName(self, roleid, allrole):
        for role in allrole:
            if role['_id'] == roleid:
                return role['name']
            return None
    def getRoleNames(self, roleids, allrole):
        rolenames = []
        for roleid in roleids:
            rolename = self.getRoleName(roleid, allrole)
            if rolename:
                rolenames.append(rolename)
        return rolenames
    def getDuty(self, dutyId, allduties):
        for duty in allduties:
            if duty['_id'] == dutyId:
                return duty
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
    def process_request(self):
        if self._op == 'get_all_user_task_exec_stat_by_time':
            print 'get all member data by time!'
            arguments = ujson.loads(self.request.body)
            datetime_type = arguments['datetime_type']
            starttime = arguments['starttime']

            result = []
            daycount = 1
            if datetime_type == 'month':
                startDate = datetime.datetime.fromtimestamp(starttime)
                daycount = calendar.monthrange(startDate.year, startDate.month)[1]
                currentdate = datetime.datetime.now()
                currenttime = time.mktime(currentdate.timetuple())
                if currenttime - starttime < daycount * 3600 *24:
                    # means user has selected current month
                    daycount = currentdate.day - 1
            print 'get statistic'
            print daycount
            alluser = Util.getAllUnderlingWithSelf(self.get_current_user(), self._user_info_coll)
            allrole = list(self._role_info_coll.find())
            allDuties = list(self._duty_info_coll.find().sort('starttime', 1))
            if alluser and allrole:
                for user in alluser:
                    print 'get statistic data for user:' + user['name']
                    # get all duties for this user
                    userDuties = user['duty']
                    userRoles = user['role']
                    userRoleNames = self.getRoleNames(userRoles, allrole)

                    userAllDutyCount = daycount * len(userDuties)
                    queryStartDate = starttime
                    queryEndDate = starttime + daycount * 3600 * 24
                    taskExecInfo = self._task_exec_data_coll.find({'userid': user['_id'], 'startofday': {'$gte': queryStartDate, '$lt': queryEndDate}})
                    finishCount = 0
                    if taskExecInfo:
                        for taskexec in taskExecInfo:
                            realendtime = taskexec['realendtime']
                            duty = self.getDuty(taskexec['taskid'], allDuties)
                            taskStarttime = duty['starttime'] + taskexec['startofday']
                            taskEndtime = duty['endtime'] + taskexec['startofday']
                            if realendtime < taskEndtime + 600 or taskexec['approve_status'] == '1':
                                finishCount += 1

                    item = {}
                    item['userid'] = user['_id']
                    item['username'] = user['name']
                    item['role'] = ' '.join(userRoleNames)
                    item['unfinish_count'] = userAllDutyCount - finishCount
                    if item['unfinish_count'] < 0:
                        item['unfinish_count'] = 0
                    result.append(item)
            print '***************************'
            print result
            self.json_result = result
        elif self._op == 'get_all_user_task_exec_stat_by_date_range':
            print 'get all member data by time range!'
            arguments = ujson.loads(self.request.body)
            starttime = arguments['starttime']
            endtime = arguments['endtime']

            result = []
            startDate = datetime.datetime.fromtimestamp(starttime)
            endDate = datetime.datetime.fromtimestamp(endtime)
            daycount = (endDate - startDate).days
            alluser = Util.getAllUnderlingWithSelf(self.get_current_user(), self._user_info_coll)
            allrole = list(self._role_info_coll.find())
            allDuties = list(self._duty_info_coll.find().sort('starttime', 1))
            if alluser and allrole:
                for user in alluser:
                    print 'get statistic data for user:' + user['name']
                    # get all duties for this user
                    userDuties = user['duty']
                    userRoles = user['role']
                    userRoleNames = self.getRoleNames(userRoles, allrole)

                    userAllDutyCount = daycount * len(userDuties)
                    queryStartDate = starttime
                    queryEndDate = endtime
                    taskExecInfo = self._task_exec_data_coll.find({'userid': user['_id'], 'startofday': {'$gte': queryStartDate, '$lt': queryEndDate}})
                    finishCount = 0
                    if taskExecInfo:
                        for taskexec in taskExecInfo:
                            realendtime = taskexec['realendtime']
                            duty = self.getDuty(taskexec['taskid'], allDuties)
                            taskStarttime = duty['starttime'] + taskexec['startofday']
                            taskEndtime = duty['endtime'] + taskexec['startofday']
                            if realendtime < taskEndtime + 600 or taskexec['approve_status'] == '1':
                                finishCount += 1

                    item = {}
                    item['userid'] = user['_id']
                    item['username'] = user['name']
                    item['role'] = ' '.join(userRoleNames)
                    item['unfinish_count'] = userAllDutyCount - finishCount
                    if item['unfinish_count'] < 0:
                        item['unfinish_count'] = 0
                    result.append(item)

            self.json_result = result
        elif self._op == 'get_user_notify_info_by_date':
            print 'get user notify info by date!'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']

            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userDuties = user['duty']
                groupDuties = self.getUserGroupDuty(user['_id'])
                if len(groupDuties) > 0:
                    userDuties = userDuties + groupDuties

                allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}}).sort('starttime', 1)

            result = []
            startofday = arguments['startofday']
            for index, duty in enumerate(allUserDuties):
                if not self.shouldPickDuty(duty, startofday):
                    # 如果此职责不需要显示在查询的date的职责列表上的话，直接跳过
                    continue
                if not duty['notify_user'] \
                        or not 'notify_user_setting_list' in duty \
                        or len(duty['notify_user_setting_list']) == 0:
                    continue
                dutyId = duty['_id']
                query = {'userid': userid, 'taskid': dutyId, 'startofday': startofday}
                data = self._task_exec_data_coll.find_one(query)
                notify = {}
                if not data:
                    notify['userid'] = userid
                    notify['taskid'] = dutyId
                    notify['startofday'] = startofday

                result.append(notify)

            self.json_result = result
        super(NotifyHandler, self).process_request()


