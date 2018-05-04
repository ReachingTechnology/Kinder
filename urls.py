#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import tornado.web

from backend.handler.auth.LoginHandler import LoginHandler
from backend.handler.auth.LogoutHandler import LogoutHandler
# from backend.handler.userLogin import UserLogin
from backend.handler.query.QueryHandler import QueryHandler
from backend.handler.management.UserAccountHandler import UserAccountHandler
from backend.handler.management.UserRoleHandler import UserRoleHandler
from backend.handler.management.UserPermissionHandler import UserPermissionHandler
from backend.handler.management.TaskHandler import TaskHandler
from backend.handler.management.DutyHandler import DutyHandler
from backend.handler.commit.TaskExecActionHandler import TaskExecActionHandler
from backend.handler.management.UserLocationHandler import UserLocationHandler
from backend.handler.management.InformHandler import InformHandler
from backend.handler.util.UploadImage import UploadImage
from backend.handler.management.DocumentHandler import DocumentHandler

URLS = [
    # (r"/user/login", LoginHandler, {'op':'login'}),
    # (r"/login", UserLogin),
    (r"/management/get_location_center", UserLocationHandler, {'op':'get_location_center'}),
    (r"/user/get_current_user", LoginHandler, {'op':'get_current_user'}),
    (r"/user/user_login", LoginHandler, {'op':'login'}),
    (r"/user/user_logout", LogoutHandler, {'op':'logout'}),
    (r"/user/change_pass", UserAccountHandler, {'op':'change_pass'}),

    (r"/management/upsert_user", UserAccountHandler, {'op':'upsert_user'}),
    (r"/management/remove_user", UserAccountHandler, {'op':'remove_user'}),
    (r"/management/query_all_user", UserAccountHandler, {'op':'query_all_user'}),
    (r"/management/set_user_avatar", UserAccountHandler, {'op':'set_user_avatar'}),

    (r"/management/upsert_user_group", UserAccountHandler, {'op':'upsert_user_group'}),
    (r"/management/remove_user_group", UserAccountHandler, {'op':'remove_user_group'}),
    (r"/management/query_all_user_group", UserAccountHandler, {'op':'query_all_user_group'}),

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
    (r"/management/query_all_duty_category", DutyHandler, {'op':'query_all_duty_category'}),
    (r"/management/upsert_duty_category", DutyHandler, {'op':'upsert_duty_category'}),
    (r"/management/remove_duty_category", DutyHandler, {'op':'remove_duty_category'}),

    (r"/manager/get_all_user_task_exec_stat_by_time", QueryHandler, {'op':'get_all_user_task_exec_stat_by_time'}),
    (r"/manager/get_all_user_task_exec_stat_by_date_range", QueryHandler, {'op':'get_all_user_task_exec_stat_by_date_range'}),

    (r"/user/get_task_exec_info_by_date", TaskExecActionHandler, {'op':'get_task_exec_info_by_date'}),
    (r"/user/mobile_get_task_exec_info_by_date", TaskExecActionHandler, {'op':'mobile_get_task_exec_info_by_date'}),
    (r"/user/get_user_task_exec_info_by_daterange", TaskExecActionHandler, {'op':'get_user_task_exec_info_by_daterange'}),
    (r"/user/get_one_task_exec_info_by_daterange", TaskExecActionHandler, {'op': 'get_one_task_exec_info_by_daterange'}),
    (r"/user/commit_task_exec_info", TaskExecActionHandler, {'op':'commit_task_exec_info'}),

    (r"/management/query_all_user_location", UserLocationHandler, {'op':'query_all_user_location'}),
    (r"/management/upsert_user_location", UserLocationHandler, {'op':'upsert_user_location'}),

    (r"/inform/query_all_inform", InformHandler, {'op':'query_all_inform'}),
    (r"/inform/upsert_inform", InformHandler, {'op':'upsert_inform'}),
    (r"/inform/remove_inform", InformHandler, {'op':'remove_inform'}),
    (r"/inform/get_new_duty_notification_by_user", InformHandler, {'op':'get_new_duty_notification_by_user'}),
    (r"/inform/get_all_duty_notification_by_user", InformHandler, {'op':'get_all_duty_notification_by_user'}),
    (r"/inform/get_underline_duty_notification_by_user", InformHandler, {'op':'get_underline_duty_notification_by_user'}),
    (r"/inform/get_new_inform_by_user", InformHandler, {'op':'get_new_inform_by_user'}),
    (r"/inform/get_all_inform_by_user", InformHandler, {'op':'get_all_inform_by_user'}),
    (r"/inform/check_single_notification", InformHandler, {'op':'check_single_notification'}),
    (r"/inform/check_single_inform", InformHandler, {'op':'check_single_inform'}),
    (r"/inform/get_new_duty_notification_count", InformHandler, {'op':'get_new_duty_notification_count'}),
    (r"/inform/get_new_inform_count", InformHandler, {'op':'get_new_inform_count'}),
    (r"/inform/remove_user_inform", InformHandler, {'op':'remove_user_inform'}),
    (r"/inform/remove_user_notification", InformHandler, {'op':'remove_user_notification'}),

    (r"/document/get_document_list", DocumentHandler, {'op':'get_document_list'}),
    (r"/document/upload_document_country", DocumentHandler, {'op':'upload_document_country'}),
    (r"/document/upload_document_city", DocumentHandler, {'op': 'upload_document_city'}),
    (r"/document/upload_document_kindergarten", DocumentHandler, {'op': 'upload_document_kindergarten'}),
    (r"/document/remove_document", DocumentHandler, {'op':'remove_document'}),

    (r"/util/uploadimage", UploadImage)
]
