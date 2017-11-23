#!/usr/bin/python
# -*- coding: utf-8 -*-
#

class UserManager(object):
    USER_SESSION_KEY_FMT = "session:%s"

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.options = {
            'key_prefix': 'session_kinder',
            'expire': 3600,
        }

    def prefixed(self, sid):
        return '%s:%s' % (self.options['key_prefix'], sid)

    def initialize(self, redisProxy, **options):
        self._redisProxy = redisProxy
        self.options.update(options)

    def add_user(self, name, value):
        self._redisProxy.set_value_to_cache(self.prefixed(name), value, self.options['expire'], pack=True)

    def remove_user(self, name):
        self._redisProxy.delete_value_from_redis(self.prefixed(name))

    def set_user_data(self, key, value, expired=3600, pack=True):
        self._redisProxy.set_value_to_cache(key, value, expired, pack)

    def get_user_data(self, key, pack=True):
        return self._redisProxy.get_value_from_redis(key, pack)

    # def get_user_attr(self, name, attr):
    #     userInfo = self._redisProxy.get_value_from_redis(self.prefixed(name), pack=True)
    #     if userInfo:
    #         return userInfo.get(attr)
    #     else:
    #         return None
    #
    # def has_func(self, user, func):
    #     userInfo = self.get_user_attr(user, 'auth_path')
    #     try:
    #         if func in userInfo:
    #             return True
    #         else:
    #             return False
    #     finally:
    #         pass

    def access(self, name):
        key = self.prefixed(name)
        redisConn, redisNode = self._redisProxy.get_connection(key)
        return redisConn.expire(key, self.options['expire'])