#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const

class TaskHandler(AsynchronousHandler):
    
    def initialize(self, op):
        self._op = op
        self._task_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_info")

    def process_request(self):
        if self._op == 'query_all_task':
            print 'query all task!'
            tasks = self._task_info_coll.find()
            self.json_result = tasks
        elif self._op == 'remove_task':
            print 'remove task!'
            taskid = self.get_argument("_id")
            self._task_info_coll.remove({"_id": taskid})
            self.json_result = {'status': 0}
        elif self._op == 'upsert_task':
            arguments = ujson.loads(self.request.body)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']
            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['starttime'] = arguments["starttime"]
            item['endtime'] = arguments["endtime"]
            item['type'] = arguments['type']
            item['upper_role'] = arguments['upper_role']
            self._task_info_coll.save(item)
            self.json_result = {'status': 0}

        super(TaskHandler, self).process_request()


