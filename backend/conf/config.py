#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import logging
import ujson

MONGO_ID_COUNTER = "id_generator"
DEVICE_COLL_NAME = "device"
BRAND_COLL_NAME = "brand"
PROVIDER_COLL_NAME = "provider"
OP_LOG_COLL_NAME = "operation_log"
COUNTRY_COLL_NAME = "country"
ACTIVITY_COLL_NAME = "activity"
DEVICE_BRAND_COLL_NAME = "devicebrands"
LOCATION_COLL_NAME = "location"
CONFIG_COLL_NAME = "config"


class _Config(object):
    def __init__(self):
        self._logger = None

    def convert(self, input_content):
        if isinstance(input_content, dict):
            if not input_content:
                return {}
            ret_set = {}
            for key, value in input_content.iteritems():
                ret_set[self.convert(key)] = self.convert(value)
            return ret_set
        elif isinstance(input_content, list):
            if not input_content:
                return []
            return [self.convert(element) for element in input_content]
        elif isinstance(input_content, unicode):
            return input_content.encode('utf-8')
        else:
            return input_content

    def load_setting_json(self, filename):
        self._filename = filename
        self.reload_setting_json()

    def reload_setting_json(self):
        with open(self._filename, mode='r') as file_object:
            data = file_object.read()
            setting = ujson.loads(data)
            setting = self.convert(setting)

            self._controller_mongo = setting.get('CONTROLLER_MONGO_DATABASE')
            self._tvcat_mongo = setting.get('TVCAT_MONGO_DATABASE')
            self._kinder_mongo = setting.get('KINDER_MONGO_DATABASE')
            self._dvb_mongo = setting.get('DVB_MONGO_DATABASE')
            self._assistant_mongo = setting.get('ASSISTANT_MONGO_DATABASE')
            self._mysql = setting.get('MYSQL_DATABASE')
            self._redis_data = setting.get('REDIS_DATA')
            self._domain = setting.get('domain')
            self._logfile = setting.get('LOG_PATH')
            self._debug = setting.get('DEBUG')
            self._page_size = setting.get('default_page_size')

            self._cas = setting.get("CAS_SETTINGS")
            self._email = setting.get('EMAIL')
            self._cluster_num = setting.get('CLUSTER_NUM')
            self._upload_cong = setting.get('UPLOAD_CONF')
            self._mfs = setting.get('mfs_upload_url')
            self._redis_event_config = setting.get('CONTROLLER_REDIS_EVENT')
            self._refresh_brand = setting.get('REDIS_REFRESH_BRAND')
            self._refresh_device = setting.get('REDIS_REFRESH_DEVICE')
            self._refresh_version = setting.get('REDIS_REFRESH_VERSION')
            self._refresh_country = setting.get('REDIS_REFRESH_COUNTRY')
            self._refresh_activity = setting.get('REDIS_REFRESH_ACTIVITY')
            self._refresh_lineup = setting.get('REDIS_REFRESH_LINEUP')
            self._refresh_solr = setting.get('REDIS_REFRESH_SOLR')
            self._refresh_device_brand = setting.get('REDIS_REFRESH_DEVICE_BRAND')
            self._refresh_config = setting.get('REDIS_REFRESH_CONFIG')

            self._redis_tvcat_event_config = setting.get('TVCAT_REDIS_EVENT')
            self._refresh_tvcat_config = setting.get('REDIS_REFRESH_TVCAT_CONFIG')
            self._refresh_tvcat_channel = setting.get('REDIS_REFRESH_TVCAT_CHANNEL')
            self._refresh_tvcat_info = setting.get('REDIS_REFRESH_TVCAT_INFO')
            self._refresh_tvcat_recommend = setting.get('REDIS_REFRESH_TVCAT_RECOMMEND')
            self._refresh_tvcat_rcepg_home = setting.get('REDIS_REFRESH_TVCAT_RCEPG_HOME')
            self._refresh_tvcta_aspect = setting.get('REDIS_REFRESH_TVCAT_ASPECT')
            self._refresh_tvcta_cust_event = setting.get('REDIS_REFRESH_TVCAT_CUST_EVENT')
            self._refresh_tvcta_customize_data = setting.get('REDIS_REFRESH_TVCAT_CUSTOMIZE_DATA')
            self._backup_apk_url = setting.get('BACKUP_APK_URL')
            self._mongo_db_name = setting.get('CONTROLLER_DB_NAME')
            if self._logger:
                self._logger.warn("Load setting config: %s", data)

    def init_logger(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def controller_mongo(self):
        return self._controller_mongo

    @property
    def dvb_mongo(self):
        return self._dvb_mongo

    @property
    def tvcat_mongo(self):
        return self._tvcat_mongo

    @property
    def kinder_mongo(self):
        return self._kinder_mongo

    @property
    def assistant_mongo(self):
        return self._assistant_mongo

    @property
    def mysql(self):
        return self._mysql

    @property
    def domain(self):
        return self._domain

    @property
    def page_size(self):
        return self._page_size

    @property
    def redis_data(self):
        return self._redis_data

    @property
    def logfile(self):
        return self._logfile

    @property
    def cas(self):
        return self._cas

    @property
    def email(self):
        return self._email

    @property
    def mfs_url(self):
        return self._mfs

    @property
    def cluster_num(self):
        return self._cluster_num

    @property
    def upload_conf(self):
        return self._upload_conf

    @property
    def debug(self):
        return self._debug

    @property
    def redis_event(self):
        return self._redis_event_config

    @property
    def refresh_brand(self):
        return self._refresh_brand

    @property
    def refresh_version(self):
        return self._refresh_version

    @property
    def refresh_country(self):
        return self._refresh_country

    @property
    def refresh_activity(self):
        return self._refresh_activity

    @property
    def refresh_lineup(self):
        return self._refresh_lineup

    @property
    def refresh_config(self):
        return self._refresh_config

    @property
    def refresh_solr(self):
        return self._refresh_solr

    @property
    def refresh_device(self):
        return self._refresh_device

    @property
    def refresh_device_brand(self):
        return self._refresh_device_brand

    @property
    def redis_tvcat_event(self):
        return self._redis_tvcat_event_config

    @property
    def refresh_tvcat_config(self):
        return self._refresh_tvcat_config

    @property
    def refresh_tvcat_channel(self):
        return self._refresh_tvcat_channel

    @property
    def refresh_tvcat_info(self):
        return self._refresh_tvcat_info

    @property
    def refresh_tvcat_recommend(self):
        return self._refresh_tvcat_recommend

    @property
    def refresh_tvcat_rcepghome(self):
        return self._refresh_tvcat_rcepg_home

    @property
    def refresh_tvcat_aspect(self):
        return self._refresh_tvcta_aspect

    @property
    def refresh_tvcat_cust_event(self):
        return self._refresh_tvcta_cust_event

    @property
    def refresh_tvcat_customize_data(self):
        return self._refresh_tvcta_customize_data

    @property
    def mongo_db_name(self):
        return self._mongo_db_name

    @property
    def backup_apk_url(self):
        return self._backup_apk_url

    def convert_dict_to_list(self, dict_value, key_name, value_name):
        lists = []
        for item in dict_value:
            content = {}
            content[key_name] = item
            content[value_name] = dict_value[item]
            lists.append(content)
        return lists

    def convert_list_to_dict(self, list_value, key_name, value_name):
        dict_value = {}
        for item in list_value:
            dict_value[item.get(key_name, '')] = item.get(value_name, '')
        return dict_value


SystemConfig = _Config()
