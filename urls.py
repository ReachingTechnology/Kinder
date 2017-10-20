#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import tornado.web

from backend.handler.auth.LoginHandler import LoginHandler
from backend.handler.query.QueryHandler import QueryHandler
from backend.handler.management.UserAccountHandler import UserAccountHandler
from backend.handler.management.UserRoleHandler import UserRoleHandler
from backend.handler.management.UserPermissionHandler import UserPermissionHandler
from backend.handler.management.TaskHandler import TaskHandler
from backend.handler.management.DutyHandler import DutyHandler
from backend.handler.commit.TaskExecActionHandler import TaskExecActionHandler

URLS = [
    (r"/login", LoginHandler, {'op':'login'}),
    (r"/user/user_login", UserAccountHandler, {'op':'login'}),

    (r"/management/upsert_user", UserAccountHandler, {'op':'upsert_user'}),
    (r"/management/remove_user", UserAccountHandler, {'op':'remove_user'}),
    (r"/management/query_all_user", UserAccountHandler, {'op':'query_all_user'}),

    (r"/management/query_all_role", UserRoleHandler, {'op':'query_all_role'}),
    (r"/management/upsert_role", UserRoleHandler, {'op':'upsert_role'}),
    (r"/management/remove_role", UserRoleHandler, {'op':'remove_role'}),

    (r"/management/query_all_permission", UserPermissionHandler, {'op':'query_all_permission'}),
    (r"/management/query_all_permission_role", UserPermissionHandler, {'op':'query_all_permission_role'}),
    (r"/management/upsert_permission_role", UserPermissionHandler, {'op':'upsert_permission_role'}),
    (r"/management/remove_permission_role", UserPermissionHandler, {'op':'remove_permission_role'}),

    (r"/management/query_all_task", TaskHandler, {'op':'query_all_task'}),
    (r"/management/upsert_task", TaskHandler, {'op':'upsert_task'}),

    (r"/management/query_all_duty", DutyHandler, {'op':'query_all_duty'}),
    (r"/management/upsert_duty", DutyHandler, {'op':'upsert_duty'}),
    (r"/management/remove_duty", DutyHandler, {'op':'remove_duty'}),
    (r"/duty/query_duty_by_user", DutyHandler, {'op':'get_duty_by_user'}),

    (r"/manager/query_all_by_time", QueryHandler, {'op':'get_all_data_by_time'}),
    (r"/manager/query_all_by_time_range", QueryHandler, {'op':'get_all_data_by_time_range'}),

    (r"/user/get_task_exec_info_by_date", TaskExecActionHandler, {'op':'get_task_exec_info_by_date'}),
    (r"/user/get_user_task_exec_info_by_daterange", TaskExecActionHandler, {'op':'get_user_task_exec_info_by_daterange'}),
    (r"/user/get_one_task_exec_info_by_daterange", TaskExecActionHandler, {'op': 'get_one_task_exec_info_by_daterange'}),
    (r"/user/commit_task_exec_info", TaskExecActionHandler, {'op':'commit_task_exec_info'})
]
