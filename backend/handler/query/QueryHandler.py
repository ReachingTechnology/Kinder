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

class QueryHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._role_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "role_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")

    def getRoleName(self, roleid, allrole):
        for role in allrole:
            if role['_id'] == roleid:
                return role['name']
    def getDuty(self, dutyId, allduties):
        for duty in allduties:
            if duty['_id'] == dutyId:
                return duty
    def process_request(self):
        if self._op == 'save_item':
            result = self._user_chat_coll.find()
        elif self._op == 'get_all_data_by_time':
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
            alluser = list(self._user_info_coll.find())
            allrole = list(self._role_info_coll.find())
            allDuties = list(self._duty_info_coll.find().sort('starttime', 1))
            if alluser and allrole:
                for user in alluser:
                    print 'get statistic data for user:' + user['name']
                    # get all duties for this user
                    userDuties = []
                    userRole = user['role']
                    userRoleName = self.getRoleName(userRole, allrole)

                    if allDuties:
                        for duty in allDuties:
                            roles = duty['roles']
                            if userRole in roles:
                                userDuties.append(duty)
                    print len(userDuties)
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
                    item['role'] = userRoleName
                    item['unfinish_count'] = userAllDutyCount - finishCount
                    if item['unfinish_count'] < 0:
                        item['unfinish_count'] = 0
                    result.append(item)

            self.json_result = result

        super(QueryHandler, self).process_request()


