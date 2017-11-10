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

    def process_request(self):
        if self._op == 'query_all_user_location':
            print 'query all user location!'
            result = self._user_location_info_coll.find()
            self.json_result = result
        elif self._op == 'upsert_user_location':
            arguments = ujson.loads(self.request.body)
            item = {}
            location = self._user_location_info_coll.find({'user_id': arguments['user_id']})
            if not location:
                location = {'user_id': arguments['user_id']}
            location['locationX'] = arguments['locationX']
            location['locationY'] = arguments['locationY']
            location['update_time'] = DateUtil.get_current_time()
            self._user_location_info_coll.save(location)
            self.json_result = {'status': 0}
        super(UserLocationHandler, self).process_request()


