#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import tornado.web

class LoginHandler(tornado.web.RequestHandler):
    def initialize(self, op):
        self._op = op
        self._user_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "user_info")
    def get(self):
        self.render("login.html")
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))

        self.redirect("/")