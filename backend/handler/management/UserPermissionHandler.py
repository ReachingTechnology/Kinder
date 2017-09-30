#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime

import ujson

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const

class UserPermissionHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._permission_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "permission_info")
        self._permission_role_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "permission_role_info")

    def process_request(self):
        if self._op == 'query_all_permission':
            print 'query all permission!'
            permissions = self._permission_info_coll.find()
            self.json_result = permissions
        elif self._op == 'query_all_permission_role':
            print 'query all permission role!'
            roles = self._permission_role_info_coll.find()
            self.json_result = roles
        elif self._op == 'remove_permission_role':
            print 'remove role!'
            arguments = ujson.loads(self.request.body)
            self._permission_role_info_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'upsert_permission_role':
            arguments = ujson.loads(self.request.body)
            exisPermissionRoles = self._permission_role_info_coll.find().sort("_id", -1)
            item = {}
            if '_id' in arguments:
                item['_id'] = arguments['_id']
            else:
                item['_id'] = ''
            if item['_id'] == '':
                existCount = exisPermissionRoles.count()
                if existCount == 0:
                    newid = "PERM_ROLE_00001"
                    newseq = 1
                else:
                    lastRole = exisPermissionRoles.next()
                    newseq = lastRole['seq'] + 1
                    newid = "PERM_ROLE_{:0>5d}".format(newseq)
                item['_id'] = newid
                item['seq'] = newseq

            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['permissions'] = arguments["permissions"]
            self._permission_role_info_coll.save(item)
            self.json_result = {'status': 0}
        super(UserPermissionHandler, self).process_request()


