#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import datetime
from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
import ujson

class UserAccountHandler(AsynchronousHandler):
    QUERY_FIELDS = {"_id": 1, "description": 1}

    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
        self._user_group_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_group_info")
        self._role_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "role_info")

    def process_request(self):
        if self._op == 'login':
            print 'user login'
            arguments = ujson.loads(self.request.body)
            userid = arguments['userid']
            password = arguments['pass']

            result = self._user_info_coll.find_one({'_id': userid, 'password': password})
            if not result:
                print 'not found user by id'
                print userid
                result = self._user_info_coll.find_one({'cellphone': userid, 'password': password})
            if not result:
                print 'not found user by cellphone'
                result = {'_id': '', 'name': ''}
            self.json_result = result
        elif self._op == 'upsert_user':
            print 'add user!'
            arguments = ujson.loads(self.request.body)
            item = {}

            if '_id' in arguments:
                item['_id'] = arguments['_id']

            item['name'] = arguments["name"]
            item['role'] = arguments["role"]
            item['duty'] = arguments['duty']
            item['leader'] = arguments['leader']
            item['sex'] = arguments["sex"]
            if 'birthday' in arguments:
                item['birthday'] = arguments["birthday"]
            else:
                item['birthday'] = ''
            item['cellphone'] = arguments["cellphone"]
            item['password'] = arguments["password"]
            if item['password'] == '':
                item['password'] = item['cellphone']
            self._user_info_coll.save(item)
            self.json_result = {'status': 0}
        elif self._op == 'remove_user':
            arguments = ujson.loads(self.request.body)
            self._user_info_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'query_all_user':
            query = {"_id": {"$ne": 'admin'}}
            results = self._user_info_coll.find(query)
            self.json_result = results
        elif self._op == 'upsert_user_group':
            print 'add user group!'
            arguments = ujson.loads(self.request.body)
            existGroups = self._user_group_coll.find().sort("_id", -1)
            item = {}

            if '_id' in arguments:
                item['_id'] = arguments['_id']
            else:
                item['_id'] = ''
            if item['_id'] == '':
                existCount = existGroups.count()
                if existCount == 0:
                    newid = "USER_GROUP_001"
                    newseq = 1
                else:
                    lastGroup = existGroups.next()
                    newseq = lastGroup['seq'] + 1
                    newid = "USER_GROUP_{:0>3d}".format(newseq)
                item['_id'] = newid
                item['seq'] = newseq
            else:
                item['seq'] = arguments['seq']

            item['name'] = arguments["name"]
            item['descr'] = arguments["descr"]
            item['leader'] = arguments['leader']
            item['members'] = arguments["members"]
            self._user_group_coll.save(item)
            self.json_result = {'status': 0}
        elif self._op == 'remove_user_group':
            arguments = ujson.loads(self.request.body)
            self._user_group_coll.remove({"_id": {"$in": arguments}})
            self.json_result = {'status': 0}
        elif self._op == 'query_all_user_group':
            results = self._user_group_coll.find()
            self.json_result = results
        super(UserAccountHandler, self).process_request()


