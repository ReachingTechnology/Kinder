#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
from backend.handler.util.ArrayUtil import ArrayUtil


class DutyHandler(AsynchronousHandler):
    def initialize(self, op):
        self._op = op
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._duty_category_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_category")

    def process_request(self):
        if self._op == 'query_all_duty':
            print 'query all duty!'
            duties = self._duty_info_coll.find()
            self.json_result = duties
        elif self._op == 'get_duty_by_user':
            arguments = ujson.loads(self.request.body)
            if not 'userid' in arguments:
                self.json_result = []
                super(DutyHandler, self).process_request()
                return
            result = []
            user = self._user_info_coll.find_one({'_id': arguments['userid']})
            if user:
                userRole = user['role']
                allDuties = self._duty_info_coll.find().sort('starttime', 1)

                if allDuties:
                    for duty in allDuties:
                        roles = duty['roles']
                        if userRole in roles:
                            result.append(duty)

            self.json_result = result
        elif self._op == 'remove_duty':
            print 'remove duty!'
            arguments = ujson.loads(self.request.body)
            self._duty_info_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'upsert_duty':
            arguments = ujson.loads(self.request.body)
            existDuties = self._duty_info_coll.find().sort("_id", -1)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']
            else:
                item['_id'] = ''
            if item['_id'] == '':
                existCount = existDuties.count()
                if existCount == 0:
                    newid = "DUTY_00001"
                    newseq = 1
                else:
                    lastDuty = existDuties.next()
                    newseq = lastDuty['seq'] + 1
                    newid = "DUTY_{:0>5d}".format(newseq)
                item['_id'] = newid
                item['seq'] = newseq
            else:
                item['seq'] = arguments['seq']
            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['category'] = arguments['category']
            item['starttime'] = arguments["starttime"]
            item['endtime'] = arguments["endtime"]
            item['roles'] = arguments["roles"]
            item['timeType'] = arguments['timeType']
            item['periodType'] = arguments['periodType']
            item['periodDate'] = arguments['periodDate']
            item['notify_user'] = arguments['notify_user']
            item['notify_user_setting_list'] = arguments['notify_user_setting_list']
            item['notify_manager'] = arguments['notify_manager']
            item['notify_manager_setting_list'] = arguments['notify_manager_setting_list']
            self._duty_info_coll.save(item)

            allUser = list(self._user_info_coll.find({"_id": {"$ne": "admin"}}))
            for user in allUser:
                if ArrayUtil.isIntersect(user['role'], item['roles']):
                    if not item['_id'] in user['duty']:
                        user['duty'].append(item['_id'])
                else:
                    if item['_id'] in user['duty']:
                        user['duty'].remove(item['_id'])
                self._user_info_coll.save(user)
            self.json_result = {'status': 0}
        elif self._op == 'query_all_duty_category':
            categories = self._duty_category_coll.find()
            self.json_result = categories
        elif self._op == 'upsert_duty_category':
            arguments = ujson.loads(self.request.body)
            existCategories = self._duty_category_coll.find().sort("_id", -1)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']
            else:
                item['_id'] = ''
            if item['_id'] == '':
                existCount = existCategories.count()
                if existCount == 0:
                    newid = "DUTY_CAT_00001"
                    newseq = 1
                else:
                    lastDutyCat = existCategories.next()
                    newseq = lastDutyCat['seq'] + 1
                    newid = "DUTY_CAT_{:0>5d}".format(newseq)
                item['_id'] = newid
                item['seq'] = newseq
            else:
                item['seq'] = arguments['seq']
            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            self._duty_category_coll.save(item)
            self.json_result = {'status': 0}
        elif self._op == 'remove_duty_category':
            arguments = ujson.loads(self.request.body)
            self._duty_category_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        super(DutyHandler, self).process_request()


