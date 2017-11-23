#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2011 DuoKan
#

import datetime
import logging
import ujson
import functools

import tornado.web
import tornado.ioloop
# from utils.collections import OrderedDict
from backend.common.userManager import UserManager
from backend.common.consts import Const

# from common.jsonconst import COOKIE_USER_KEY, COOKIE_ROLE_KEY

ADMIN_USER = "admin"


class BaseHandler(tornado.web.RequestHandler):
    @tornado.web.authenticated
    def initialize(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def _check_user_login(self):
        return True
        current_user = self.get_current_user()
        if not current_user:
            # self.redirect(self.get_login_url())
            return False

        if not UserManager.instance().access(current_user):
            # self.redirect(self.get_login_url())
            return False
        #
        # self._username = self.get_user_name()
        # self._menulist = self._get_menu_pane(self.request.path)
        return True

    def _is_admin_user(self):
        # return self.get_secure_cookie(COOKIE_ROLE_KEY) == ADMIN_USER
        return True

    def get(self):
        if not self._check_user_login():
            self.set_status(401)
            self.finish()
            return

        cur_path = self.request.path
        if cur_path == '/login' or cur_path == '/logout' or self._is_admin_user():
            self.handle()
            return

        # auth_path = UserManager.instance().get_user_attr(self.current_user, 'auth_path')
        # if cur_path in auth_path:
        self.handle()
        return

        # self._logger.warn("%s does not have permission for path %s", self.current_user, cur_path)
        # self.render("not_auth.html")

    def post(self):
        if not (self.request.uri == '/user/user_login' or self.request.uri == '/user/user_logout'):
            if not self._check_user_login():
                self.set_status(401)
                self.finish()
                return

        cur_path = self.request.path
        # auth_path = UserManager.instance().get_user_attr(self.current_user, 'auth_path')
        # if (cur_path in auth_path) or self._is_admin_user():
        self.handle()
        return

        # self._logger.warn("%s does not have permission for path:%s", self.current_user, cur_path)
        # self.json_result = ujson.dumps({'auth': -1}, ensure_ascii=False)
        # self.write(self.json_result)

    def options(self):
        self.set_status(204)
        self.finish()

    def handle(self):
        raise tornado.web.HTTPError(500)

    def complete_request(self, response):
        try:
            if self.get_status() == 200:
                if isinstance(response, dict):
                    final_result = ujson.dumps(response, ensure_ascii=False)
                self.write(final_result)
                self.finish()
            else:
                self.write_error(self.get_status())
        except:
            pass

    def write_async_error(self, status_code, **kwargs):
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.write_error, status_code, **kwargs))

    def write_error(self, status_code, **kwargs):
        self.render("404.html")

    def get_current_user(self):
        return self.get_secure_cookie(Const.COOKIE_USER_KEY)

    def get_today(self):
        return str(datetime.date.today())

    def write_json_data(self, jsonData):
        if isinstance(jsonData, dict):
            jsonString = ujson.dumps(jsonData, ensure_ascii=False)
            self.write(jsonString)
        else:
            self.write(jsonData)
        self.finish()

    def _generate_full_path(self, posterName):
        imgPrefix = self.settings['img_prefix']
        return ''.join((imgPrefix, posterName))

    def _is_login_handler(self):
        return False

    def _query_one_sql_whth_begin(self, sql, *args):
        conn = self.settings['mysql_pool'].get_connection()
        try:
            conn.begin()
            conn.execute(sql, args)
            conn.commit()
            return conn.row()
        finally:
            self.settings['mysql_pool'].free_connection(conn)

    def _query_many_sql_with_begin(self, sql, *args):
        conn = self.settings['mysql_pool'].get_connection()
        try:
            conn.begin()
            conn.execute(sql, args)
            conn.commit()
            return conn.rows()
        finally:
            self.settings['mysql_pool'].free_connection(conn)

    # def get_user_name(self):
    #     return self.get_current_user()

    # def _get_menu_pane_by_name(self, name, currentPath):
    #     permissions = UserManager.instance().get_user_attr(name, 'permission')
    #     if not permissions:
    #         return []
    #     menulist = []
    #     index = 1
    #     active_index = -1
    #     permissions = OrderedDict(sorted(permissions.items(), key=lambda t: t[0]))
    #     for k, p in permissions.items():
    #         # print k,p
    #         subcount = 0
    #         menu = {}
    #         menu['title'] = p['name']
    #         menu['id'] = p['id']
    #         menu['display'] = p['display']
    #         children = []
    #         for item in p['children']:
    #             path = item['path']
    #             flag = True if path == currentPath else False
    #             subcount = subcount + 1 if item['display'] == 1 else subcount
    #             child = {'link': item['path'],
    #                      'name': item['name'],
    #                      'display': item['display'],
    #                      'active': flag}
    #             if flag == True:
    #                 active_index = index
    #             children.append(child)
    #         menu['active'] = active_index
    #         menu['subcount'] = subcount
    #         active_index = -1
    #         menu['children'] = children
    #
    #         menulist.append(menu)
    #         index += 1
    #     return menulist

    # def _get_menu_pane(self, currentPath):
    #     userKey = self.get_current_user()
    #     if userKey:
    #         return self._get_menu_pane_by_name(userKey, currentPath)
    #     else:
    #         return []
