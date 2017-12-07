#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.handler.util.DateUtil import DateUtil

class UserLocationHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._user_location_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_location_info")
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder',"user_info")
        self._task_exec_data_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "task_exec_data")

    def process_request(self):
        if self._op == 'query_all_user_location':
            print 'query all user location!'
            # result = self._user_location_info_coll.find()
            result = []
            allUser = list(self._user_info_coll.find({"_id": {"$ne": "admin"}}))
            allTaskExecData = list(self._task_exec_data_coll.find().sort('realendtime', -1))
            for user in allUser:
                for task in allTaskExecData:
                    if user['_id'] == task['userid'] and 'locationLat' in task and 'locationLng' in task and task['locationLat'] != 0 and task['locationLng'] != 0:
                        data = {}
                        data['user_id'] = task['userid']
                        data['locationLat'] = task['locationLat']
                        data['locationLng'] = task['locationLng']
                        data['update_time'] = task['realendtime']
                        result.append(data)
                        break
                index = 0
            self.json_result = result
        elif self._op == 'upsert_user_location':
            arguments = ujson.loads(self.request.body)
            item = {}
            location = self._user_location_info_coll.find({'user_id': arguments['user_id']})
            if not location:
                location = {'user_id': arguments['user_id']}
            location['locationLat'] = arguments['locationLat']
            location['locationLng'] = arguments['locationLng']
            location['update_time'] = DateUtil.get_current_time()
            self._user_location_info_coll.save(location)
            self.json_result = {'status': 0}
        super(UserLocationHandler, self).process_request()


