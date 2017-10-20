#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime
from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
import ujson
from backend.handler.util.ArrayUtil import ArrayUtil

class TaskExecActionHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")

    def process_request(self):
        if self._op == 'get_task_exec_info_by_date':
            print 'get task exec info by date!'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']

            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userRoles = user['role']
                allDuties = self._duty_info_coll.find().sort('starttime', 1)

                if allDuties:
                    for duty in allDuties:
                        roles = duty['roles']
                        if ArrayUtil.isIntersect(userRoles, roles):
                            allUserDuties.append(duty)

            result = []
            startofday = arguments['startofday']
            for index, duty in enumerate(allUserDuties):
                dutyId = duty['_id']

                query = {'userid': userid, 'taskid': dutyId, 'startofday': startofday}
                print userid + ';' + dutyId + ';'
                print startofday
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

            # find out user duties
            allUserDuties = []
            user = self._user_info_coll.find_one({'_id': userid})
            if user:
                userRoles = user['role']
                allDuties = self._duty_info_coll.find().sort('starttime', 1)

                if allDuties:
                    for duty in allDuties:
                        roles = duty['roles']
                        if ArrayUtil.isIntersect(userRoles, roles):
                            allUserDuties.append(duty)

            result = []
            startofday = arguments['startofday']
            endofday = arguments['endofday']
            dayCount = (endofday - startofday) / (3600 * 24)
            query = {'userid': userid, 'startofday': {'$gte': startofday, '$lt': endofday}}
            taskData = list(self._task_exec_data_coll.find(query))

            for index, duty in enumerate(allUserDuties):
                dutyId = duty['_id']
                finishCount = 0
                for taskexec in taskData:
                    if taskexec['taskid'] == dutyId:
                        realendtime = taskexec['realendtime']
                        taskStarttime = duty['starttime'] + taskexec['startofday']
                        taskEndtime = duty['endtime'] + taskexec['startofday']
                        if realendtime < taskEndtime + 600:
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
            endofday = arguments['endofday']
            result = []
            task = self._duty_info_coll.find_one({'_id': taskid})
            query = {'userid': userid, 'taskid': taskid, 'startofday': {'$gte': startofday, '$lt': endofday}}
            print arguments
            taskexecdata = list(self._task_exec_data_coll.find(query))
            print len(taskexecdata)
            if True:
                # taskexecdata.sort('startofday')
                dayCount = (endofday - startofday) / (3600 * 24)

                for index in range(dayCount):
                    item = {}
                    date = startofday + 3600*24*index
                    taskexecdata_cursor = 0
                    for dd in taskexecdata:
                        if dd['startofday'] < date:
                            taskexecdata_cursor += 1
                        else:
                            break

                    if taskexecdata_cursor < len(taskexecdata) and date == taskexecdata[taskexecdata_cursor]['startofday']:
                        item['startofday'] = date
                        item['realendtime'] = taskexecdata[taskexecdata_cursor]['realendtime']
                        item['comment'] = taskexecdata[taskexecdata_cursor]['comment']
                        item['approve_status'] = taskexecdata[taskexecdata_cursor]['approve_status']
                        item['approve_user'] = taskexecdata[taskexecdata_cursor]['approve_user']
                        taskexecdata_cursor += 1
                    else:
                        item['startofday'] = date
                        item['realendtime'] = 0
                        item['comment'] = ''
                        item['approve_status'] = Const.TASK_APPROVE_STATUS_NONE
                        item['approve_user'] = ''
                    item['starttime'] = task['starttime']
                    item['endtime'] = task['endtime']
                    result.append(item)
            print len(result)
            self.json_result = result
        elif self._op == 'commit_task_exec_info':
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']
            taskid = arguments['taskid']
            startofday = arguments['startofday']
            query = {'userid': userid, 'taskid': taskid, 'startofday': startofday}
            item = self._task_exec_data_coll.find_one(query)
            if not item:
                item = {}
            item['taskid'] = taskid
            item['userid'] = userid
            item['startofday'] = startofday
            item['realendtime'] = arguments["realendtime"]
            item['comment'] = arguments["comment"]
            item['approve_status'] = arguments['approve_status']
            item['approve_user'] = arguments['approve_user']
            self._task_exec_data_coll.save(item)
            self.json_result = {'status': 0}
        super(TaskExecActionHandler, self).process_request()


