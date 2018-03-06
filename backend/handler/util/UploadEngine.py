# -*- coding: utf-8 -*-


import time
from urllib import quote
import logging
import requests


class UploadEngine(object):
    MAX_RETRY_TIMES = 3

    def __init__(self, uploader_fmt):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._uploader_fmt = uploader_fmt

    def upload(self, *args):
        self._finalUrl = self._uploader_fmt % tuple(quote(item) for item in args)
        currentTimes = 0
        while currentTimes <= self.MAX_RETRY_TIMES:
            try:
                currentTimes += 1
                r = requests.get(self._finalUrl, verify=False)
                if r.status_code == 200:
                    self._logger.info("Send %s with status:%s", self._finalUrl, r.status_code)
                    response = r.json()
                    if response.get('url'):
                        return response
                    else:
                        self._logger.info("Send %s does not succeed:%s, we'll retry it", self._finalUrl, r.status_code)
                        time.sleep(3)
                        continue
                else:
                    self._logger.error("Send %s occur error:%s", self._finalUrl, r.status_code)
                    return {'status': -1, 'url': '', 'md5': ''}
            except Exception as ex:
                self._logger.error("Send file [%s] failed, due to: %s", str(args), str(ex), exc_info=1)

        return {'status': -1, 'url': '', 'md5': ''}