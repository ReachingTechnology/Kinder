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
            # allTaskExecData = list(self._task_exec_data_coll.find().sort('realendtime', -1))
            allUserLocationData = list(self._user_location_info_coll.find().sort('update_time', -1))
            for user in allUser:
                for location in allUserLocationData:
                    if user['_id'] == location['user_id'] and location['locationLat'] != 0 and location['locationLng'] != 0:
                        data = {}
                        data['user_id'] = location['user_id']
                        data['locationLat'] = location['locationLat']
                        data['locationLng'] = location['locationLng']
                        data['update_time'] = location['update_time']
                        result.append(data)
                        break
                index = 0
            self.json_result = result
        elif self._op == 'upsert_user_location':
            arguments = ujson.loads(self.request.body)
            item = {}
            item['user_id'] = arguments['user_id']
            item['locationLat'] = arguments['locationLat']
            item['locationLng'] = arguments['locationLng']
            item['update_time'] = DateUtil.get_current_time()
            self._user_location_info_coll.save(item)
            self.json_result = {'status': 0}
        super(UserLocationHandler, self).process_request()


