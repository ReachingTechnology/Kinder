#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const


class DutyHandler(AsynchronousHandler):
    def initialize(self, op):
        self._op = op
        self._duty_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "duty_info")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")

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
            item['starttime'] = arguments["starttime"]
            item['endtime'] = arguments["endtime"]
            item['roles'] = arguments["roles"]
            self._duty_info_coll.save(item)
            self.json_result = {'status': 0}
        super(DutyHandler, self).process_request()


