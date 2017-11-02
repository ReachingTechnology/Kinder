#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const

class UserRoleHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._role_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "role_info")

    def process_request(self):
        if self._op == 'query_all_role':
            print 'query all role!'
            query = {"_id": {"$ne": 'admin'}}
            roles = self._role_info_coll.find(query)
            self.json_result = roles
        elif self._op == 'remove_role':
            print 'remove role!'
            arguments = ujson.loads(self.request.body)
            self._role_info_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'upsert_role':
            arguments = ujson.loads(self.request.body)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']

            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['upper_role'] = arguments["upper_role"]
            item['permissionRoles'] = arguments['permissionRoles']
            self._role_info_coll.save(item)
            self.json_result = {'status': 0}
        super(UserRoleHandler, self).process_request()


