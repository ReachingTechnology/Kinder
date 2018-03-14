#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
from backend.handler.util.DateUtil import DateUtil
from backend.handler.util.Util import Util

class InformHandler(AsynchronousHandler):
    def initialize(self, op):
        self._op = op
        self._inform_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "inform_info")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._user_group_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_group_info")
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")
        self._user_inform_access_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', 'user_inform_access')
        self._user_duty_notification_access_coll = self.settings['kinder_mongo_pool'].get_collection('kinder',
                                                                                          'user_duty_notification_access')
        self._scanned_user_notification_list = self.settings['kinder_mongo_pool'].get_collection('kinder',
                                                                                                 "scanned_user_notification_list")
        self._scanned_user_inform_list = self.settings['kinder_mongo_pool'].get_collection('kinder',
                                                                                           "scanned_user_inform_list")

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
        if self._op == 'query_all_inform':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(InformHandler, self).process_request()
            userid = arguments['userid']
            informs = self._inform_info_coll.find({'creator': userid})
            self.json_result = informs
        elif self._op == 'get_new_duty_notification_by_user':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(InformHandler, self).process_request()
                return
            userid = arguments['userid']
            result = list(self._scanned_user_notification_list.find({'userid': userid, 'isNew': True}))
            self.json_result = result
        elif self._op == 'get_all_duty_notification_by_user':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(InformHandler, self).process_request()
                return
            pageNum = 0
            pageSize = 10
            if 'pageNum' in arguments:
                pageNum = arguments['pageNum']
            if 'pageSize' in arguments:
                pageSize = arguments['pageSize']
            userid = arguments['userid']
            result = list(self._scanned_user_notification_list.find({'userid': userid}, skip=pageNum * pageSize))
            self.json_result = result
        elif self._op == 'get_new_inform_by_user':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(InformHandler, self).process_request()
                return
            userid = arguments['userid']
            result = list(self._scanned_user_inform_list.find(
                {'userid': userid, 'isNew': True}))
            self.json_result = result
        elif self._op == 'get_all_inform_by_user':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(InformHandler, self).process_request()
                return
            pageNum = 0
            pageSize = 10
            if 'pageNum' in arguments:
                pageNum = arguments['pageNum']
            if 'pageSize' in arguments:
                pageSize = arguments['pageSize']
            userid = arguments['userid']
            result = list(self._scanned_user_inform_list.find({'userid': userid}, skip=pageNum * pageSize))
            self.json_result = result
        elif self._op == 'get_new_duty_notification_count':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = {'count': 0}
                super(InformHandler, self).process_request()
                return
            userid = arguments['userid']
            result = list(self._scanned_user_notification_list.find(
                {'userid': userid, 'isNew': True}))
            resultLen = 0
            if result:
                resultLen = len(result)
            self.json_result = {'count': resultLen}
        elif self._op == 'get_new_inform_count':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = {'count': 0}
                super(InformHandler, self).process_request()
                return
            userid = arguments['userid']
            result = list(self._scanned_user_inform_list.find(
                {'userid': userid, 'isNew': True}))
            resultLen = 0
            if result:
                resultLen = len(result)
            self.json_result = {'count': resultLen}
        elif self._op == 'check_single_notification':
            arguments = ujson.loads(self.request.body)
            item = self._scanned_user_notification_list.find_one({'_id': arguments['_id']})
            if item:
                item['isNew'] = False
            self._scanned_user_notification_list.save(item)
            self.json_result = {'status': 0}
        elif self._op == 'check_single_inform':
            arguments = ujson.loads(self.request.body)
            item = self._scanned_user_inform_list.find_one({'_id': arguments['_id']})
            if item:
                item['isNew'] = False
            self._scanned_user_inform_list.save(item)
            self.json_result = {'status': 0}
        # elif self._op == 'get_underline_duty_notification_by_user':
        #     arguments = ujson.loads(self.request.body)
        #     if not 'userid' in arguments:
        #         self.json_result = []
        #         super(InformHandler, self).process_request()
        #         return
        #     userid = arguments['userid']
        #     userAccess = self._user_duty_notification_access_coll.find_one({'userid': userid})
        #     userLastAccessTime = 0
        #     if userAccess:
        #         userLastAccessTime = userAccess['lastAccessTime']
        #     else:
        #         userAccess = {}
        #     queryTime = DateUtil.get_current_time()
        #     startofday = arguments['startofday']
        #     allUserDuties = []
        #     result = []
        #     allUnderlineUsers = Util.getAllUnderling(userid, self._user_info_coll)
        #     if len(allUnderlineUsers) > 0:
        #         for user in allUnderlineUsers:
        #             userDuties = user['duty']
        #             groupDuties = self.getUserGroupDuty(user['_id'])
        #             if len(groupDuties) > 0:
        #                 userDuties = userDuties + groupDuties
        #             allUserDuties = self._duty_info_coll.find({"_id": {"$in": userDuties}}).sort('starttime', 1)
        #
        #             for index, duty in enumerate(allUserDuties):
        #                 if not self.shouldPickDuty(duty, startofday) or not duty['notify_manager']:
        #                     # 如果此职责不需要显示在查询的date的职责列表上的话，直接跳过
        #                     continue
        #                 dutyId = duty['_id']
        #                 if 'notify_user_setting_list' in duty and len(duty['notify_manager_setting_list']) > 0:
        #                     query = {'userid': user['_id'], 'taskid': dutyId, 'startofday': startofday}
        #                     data = self._task_exec_data_coll.find_one(query)
        #                     item = {}
        #                     if not data:
        #                         dutyRealStarttime = duty['startime'] if (duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC) else startofday + duty['starttime']
        #                         dutyRealEndtime = duty['endtime'] if (duty['timeType'] == Const.DUTY_TIME_TYPE_SPECIFIC) else startofday + duty['endtime']
        #                         for notify in duty['notify_user_setting_list']:
        #                             match = False
        #                             if notify['timeType'] == Const.NOTIFY_TIME_TYPE_BEFORE \
        #                                 and queryTime >= (dutyRealStarttime - notify['timeLength'] * 60 > userLastAccessTime):
        #                                 item['informSendTime'] = (dutyRealStarttime - notify['timeLength'] * 60)
        #                                 match = True
        #                             elif notify['timeType'] == Const.NOTIFY_TIME_TYPE_AFTER \
        #                                 and queryTime >= (dutyRealEndtime + notify['timeLength'] * 60 > userLastAccessTime):
        #                                 item['informSendTime'] = (dutyRealEndtime + notify['timeLength'] * 60)
        #                                 match = True
        #                             elif notify['timeType'] == Const.NOTIFY_TIME_TYPE_SPECIFIC \
        #                                 and (queryTime >= notify['timePoint']  > userLastAccessTime):
        #                                 item['informSendTime'] = notify['timePoint']
        #                                 match = True
        #
        #                             if match:
        #                                 item['_id'] = '{:s}_{:s}_{:s}_{:d}_{:s}'.format(userid, user['_id'], dutyId, startofday, notify['timeType'])
        #                                 item['userid'] = user['_id']
        #                                 item['taskid'] = dutyId
        #                                 item['taskname'] = duty['name']
        #                                 item['taskDescr'] = duty['descr']
        #                                 item['realstarttime'] = dutyRealStarttime
        #                                 item['realendtime'] = dutyRealEndtime
        #                                 item['dutyTimeType'] = duty['timeType']
        #                                 item['notifyTimeType'] = notify['timeType']
        #                                 item['notifyType'] = notify['notifyType']
        #                                 item['notifyPriority'] = notify['notifyPriority']
        #                                 item['createTime'] = queryTime
        #                                 result.append(item)
        #         userAccess['userid'] = userid
        #         userAccess['lastAccessTime'] = queryTime
        #         self._user_duty_notification_access_coll.save(userAccess)
        #     self.json_result = result
        elif self._op == 'remove_inform':
            arguments = ujson.loads(self.request.body)
            self._inform_info_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'upsert_inform':
            arguments = ujson.loads(self.request.body)
            existInforms = self._inform_info_coll.find().sort("_id", -1)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']
            else:
                item['_id'] = ''
            if item['_id'] == '':
                existCount = existInforms.count()
                if existCount == 0:
                    newid = "INFORM_00001"
                    newseq = 1
                else:
                    lastInform = existInforms.next()
                    newseq = lastInform['seq'] + 1
                    newid = "INFORM_{:0>5d}".format(newseq)
                item['_id'] = newid
                item['seq'] = newseq
            else:
                item['seq'] = arguments['seq']
            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['notifyType'] = arguments['notifyType']
            item['notifyPriority'] = arguments["notifyPriority"]
            item['sendTime'] = arguments["sendTime"]
            item['sender'] = arguments['sender']
            item['creator'] = self.get_current_user()
            item['informUserList'] = arguments["informUserList"]
            self._inform_info_coll.save(item)
            self.json_result = {'status': 0}
        elif self._op == 'remove_user_inform':
            arguments = ujson.loads(self.request.body)
            self._scanned_user_inform_list.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'remove_user_notification':
            arguments = ujson.loads(self.request.body)
            self._scanned_user_notification_list.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        super(InformHandler, self).process_request()


