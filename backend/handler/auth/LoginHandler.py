#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

from backend.handler.async_handler import AsynchronousHandler
from backend.common.consts import Const
from backend.common.userManager import UserManager
import ujson

class LoginHandler(AsynchronousHandler):
    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")

    def save_user_info(self, name):
        UserManager.instance().add_user(name, name)
        self.set_secure_cookie(Const.COOKIE_USER_KEY, name)


    def process_request(self):
        if self._op == 'login':
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
            else:
                self.save_user_info(userid)

            self.json_result = result
            super(LoginHandler, self).process_request()
