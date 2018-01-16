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
from backend.handler.util.DateUtil import DateUtil
from backend.handler.util.ArrayUtil import ArrayUtil

class QueryHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._role_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "role_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")
        self._user_group_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_group_info")

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
    def getUserGroupDuty(self, userId):
        duties = []
        userGroups = self._user_group_info_coll.find()
        if userGroups:
            for group in userGroups:
                if userId in group['members']:
                    duties = duties + group['duty']
        return duties
    def process_request(self):
        if self._op == 'save_item':
            result = self._user_chat_coll.find()
        elif self._op == 'get_all_user_task_exec_stat_by_time':
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
            alluser = Util.getAllUnderling(self.get_current_user(), self._user_info_coll)
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
                    queryEndDate = starttime + daycount
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
        elif self._op == 'get_all_user_task_exec_stat_by_date_range':
            print 'get all member data by time range!'
            arguments = ujson.loads(self.request.body)
            starttime = arguments['starttime']
            endtime = arguments['endtime'] + 3600 * 24 - 1

            result = []
            now = DateUtil.get_current_time()
            today = DateUtil.get_startof_today()
            startDate = datetime.datetime.fromtimestamp(starttime)
            endDate = datetime.datetime.fromtimestamp(endtime)
            daycount = DateUtil.getWorkDays(startDate, endDate)
            alluser = Util.getAllUnderling(self.get_current_user(), self._user_info_coll)
            allrole = list(self._role_info_coll.find())
            allDuties = list(self._duty_info_coll.find().sort('starttime', 1))
            if alluser and allrole:
                for user in alluser:
                    print 'get statistic data for user:' + user['name']
                    # get all duties for this user
                    userDuties = user['duty']
                    groupDuties = self.getUserGroupDuty(user['_id'])
                    if len(groupDuties) > 0:
                        userDuties = ArrayUtil.noDuplicateJoin(userDuties, groupDuties)
                    userRoles = user['role']
                    userRoleNames = self.getRoleNames(userRoles, allrole)
                    userAllDutyCount = 0
                    for dutyId in userDuties:
                        duty = self.getDuty(dutyId, allDuties)
                        if duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
                            if endtime >= duty['starttime'] and starttime <= duty['endtime']:
                                userAllDutyCount += 1
                        if duty['timeType'] == Const.DUTY_TIME_TYPE_ROUTINE:
                            userAllDutyCount += daycount
                        if duty['timeType'] == Const.DUTY_TIME_TYPE_PERIODICAL:
                            userAllDutyCount += DateUtil.getPeriodicalWorkDays(startDate, endDate, duty['periodType'], duty['periodDate'])

                    queryStartDate = starttime
                    queryEndDate = endtime
                    taskExecInfo = self._task_exec_data_coll.find({'userid': user['_id'], 'startofday': {'$gte': queryStartDate, '$lt': queryEndDate}})
                    finishCount = 0
                    approveCount = 0
                    if taskExecInfo:
                        for taskexec in taskExecInfo:
                            realendtime = taskexec['realendtime']
                            if taskexec['finish_status'] == Const.TASK_STATUS_FINISHED:
                                duty = self.getDuty(taskexec['taskid'], allDuties)
                                if duty:
                                    if duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC:
                                        taskEndtime = duty['endtime']
                                        if realendtime <= taskEndtime + 3600 * 24 or taskexec['approve_status'] == '1':
                                            finishCount += 1
                                    else:
                                        realendtime = taskexec['realendtime']
                                        # taskStarttime = duty['starttime'] + taskexec['startofday']
                                        # taskEndtime = duty['endtime'] + taskexec['startofday']
                                        if realendtime < taskexec['startofday'] + 3600 * 24 or taskexec['approve_status'] == '1':
                                            # 只要是当天提交的就可以算完成
                                            finishCount += 1
                            elif taskexec['approve_status'] != Const.TASK_APPROVE_STATUS_NONE:
                                approveCount += 1
                    item = {}
                    item['userid'] = user['_id']
                    item['username'] = user['name']
                    item['role'] = ' '.join(userRoleNames)
                    item['unfinish_count'] = userAllDutyCount - finishCount
                    item['finish_count'] = finishCount
                    item['approved_count'] = approveCount

                    if item['unfinish_count'] < 0:
                        item['unfinish_count'] = 0
                    result.append(item)

            self.json_result = result
        super(QueryHandler, self).process_request()


