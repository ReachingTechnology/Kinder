# #!/usr/bin/python
# # -*- coding: utf-8 -*-
# #
# import time
# # import ldap
# import tornado.web
#
# from utils.collections import OrderedDict
# from handler.base import BaseHandler
# from common.jsonconst import COOKIE_USER_KEY, REQ_USER_NAME, REQ_USER_PWD
# from conf.config import SystemConfig
# from storage.usermanager import UserManager
# from urllib import urlencode
#
# QUERY_USER_BY_PWD = "SELECT id from t_cms_user where name=%s and password=PASSWORD(%s)"
# QUERY_USER_BY_NAME = "SELECT id from t_cms_user where name=%s"
# QUERY_USER_PERMISSION_SQL = "SELECT distinct c.id, c.name, c.path, c.parent,c.display FROM t_cms_user_role a, t_cms_role_permission b,t_cms_permission c \
#       WHERE a.userid=%s AND a.roleid = b.roleid AND b.permissionid = c.id ORDER BY c.rank ASC"
#
# QUERY_USER_ROLE = "select code from t_cms_role a left join t_cms_user_role b on a.id=b.roleid left join t_cms_user c on b.userid=c.id where c.name=%s"
#
#
# class OwnUserLogin(BaseHandler):
#     def get(self):
#         self.render('login.html', error=False)
#
#
# class UserLogin(BaseHandler):
#     def get(self):
#         username = self.current_user
#         if not username or not UserManager.instance().access(username):
#             self._cas_login()
#             # self.render('login.html', error=False)
#             return
#
#         menulist = self._get_menu_pane_by_name(username, '')
#         self.render("welcome.html", username=username, sysname=self.settings['system_name'], menulist=menulist)
#
#     @tornado.web.asynchronous
#     def post(self):
#         try:
#             self.settings['thread_pool'].add_task(self.process_request, callback=None)
#         except Exception as ex:
#             self._logger.error("Cann't add task to thread pool, due to :%s", ex, exc_info=1)
#             self.write_error(404)
#
#     def save_user_info(self, name):
#         self.set_secure_cookie(COOKIE_USER_KEY, name)
#         row = self._query_one_sql_whth_begin(QUERY_USER_ROLE, name)
#         self.set_secure_cookie("role", row['code'])
#
#     def process_request(self):
#         try:
#             name = str(self.get_argument(REQ_USER_NAME))
#             pwd = str(self.get_argument(REQ_USER_PWD))
#             if self._auth_user_no_password(name):
#                 self.save_user_info(name)
#                 menulist = self._get_menu_pane_by_name(name, '')
#                 self.render("welcome.html", username=name, sysname=self.settings['system_name'], menulist=menulist)
#             else:
#                 self.render('login.html', error=True)
#         except Exception as ex:
#             self._logger.error("UserLogin error:%s", str(ex), exc_info=1)
#             self.write_async_error(404)
#
#     def _cas_login(self):
#         url = SystemConfig.cas['cas_server'] + "/" + "login?" + urlencode({"service": SystemConfig.cas['service_url']})
#         self.redirect(url)
#
#     def _store_user_profile(self, name, row):
#         (permission, auth_path) = self._load_user_permissions(row['id'])
#         userInfo = {'auth_path': auth_path, 'permission': permission,
#                     'login_time': int(time.time())}  ##add role and permission@mark
#         UserManager.instance().add_user(name, userInfo)
#         return True
#
#     def _auth_user_no_password(self, name):
#         row = self._query_one_sql_whth_begin(QUERY_USER_BY_NAME, name)
#         if row:
#             return self._store_user_profile(name, row)
#         else:
#             return False
#
#     def _load_user_permissions(self, userid):
#         permissions = OrderedDict()
#         tmp = {}
#         auth_path = []
#         rows = self._query_many_sql_with_begin(QUERY_USER_PERMISSION_SQL, userid)
#         for row in rows:
#
#             if 'path' in row:
#                 auth_path.append(row['path'])
#
#             permissionid = row['id']
#             parentid = row['parent']
#             checkKey = permissionid if parentid == 0 else parentid
#             if permissions.has_key(checkKey):
#                 permissions[checkKey]['children'].append(row)
#             else:
#                 if parentid == 0:
#                     permissions[permissionid] = {'name': row['name'], 'display': row['display'], 'children': [],
#                                                  'id': permissionid}
#                     if tmp.has_key(permissionid):
#                         for v in tmp[permissionid]:
#                             permissions[permissionid]['children'].append(v)
#                         del tmp[permissionid]
#                 else:
#                     if not tmp.has_key(parentid):
#                         tmp[parentid] = []
#                     tmp[parentid].append(row)
#         return (permissions, auth_path)
#
