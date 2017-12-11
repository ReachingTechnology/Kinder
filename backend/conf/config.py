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

            self._kinder_mongo = setting.get('KINDER_MONGO_DATABASE')
            self._redis_data = setting.get('REDIS_DATA')
            self._domain = setting.get('domain')
            self._logfile = setting.get('LOG_PATH')
            self._debug = setting.get('DEBUG')
            self._page_size = setting.get('default_page_size')

            self._cluster_num = setting.get('CLUSTER_NUM')
            self._upload_cong = setting.get('UPLOAD_CONF')
            self._mfs = setting.get('mfs_upload_url')

            if self._logger:
                self._logger.warn("Load setting config: %s", data)

    def init_logger(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def kinder_mongo(self):
        return self._kinder_mongo

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
