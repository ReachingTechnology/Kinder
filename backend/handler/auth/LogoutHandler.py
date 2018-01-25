#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

from backend.handler.async_handler import AsynchronousHandler
import tornado.web
from backend.common.consts import Const
from backend.common.userManager import UserManager

class LogoutHandler(AsynchronousHandler):
    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")

    def save_user_info(self, name):
        self.set_secure_cookie(Const.COOKIE_USER_KEY, name)

    def process_request(self):

        userKey = self.get_current_user()
        UserManager.instance().remove_user(userKey)
        self.clear_cookie(Const.COOKIE_USER_KEY)
        result = {'_id': '', 'name': ''}
        self.json_result = result
        super(LogoutHandler, self).process_request()