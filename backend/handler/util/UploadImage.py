#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import urllib2
import ujson

from datetime import datetime

from backend.conf.config import SystemConfig
from backend.handler.async_handler import AsynchronousHandler


class UploadImage(AsynchronousHandler):
    UPLOAD_EMPTY = 0
    UPLOAD_SUCCESS = 1
    UPLOAD_FAILED = 0
    UPLOAD_DONT_MATCH_REQUIRE = 0

    def check_xsrf_cookie(self):
        pass

    def push_file_to_cdn(self, filepath):
        headers = {"Content-type": "application/json"
            , "Accept": "text/plain"}
        request_url = SystemConfig.mfs_url % (filepath)
        request = urllib2.Request(request_url, headers=headers)
        response = urllib2.urlopen(request, timeout=600)
        infostr = response.read()
        self._logger.info(infostr)
        return ujson.loads(infostr)

    def process_request(self):
        try:
            self.json_result = {}
            data = {}
            if self.request.files:
                # file_para = self.get_arguments('input_name', [])[0]
                f = self.request.files['file'][0]
                try:
                    resp = {}
                    filename = f["filename"]
                    root, ext = os.path.splitext(filename)
                    current_time_str = str(time.time())
                    transition_filename = Util.get_str_md5(current_time_str + filename) + ext
                    now = datetime.now()
                    self._logger.info(self.settings['img_upload_path'])
                    relativePath = os.sep.join(
                        (self.settings['img_upload_path'], str(now.year), str(now.month), str(now.day)))
                    iconFilePath = os.sep.join((relativePath, transition_filename))  # 完整路径
                    self._logger.info(iconFilePath)
                    if not os.path.exists(relativePath):
                        os.makedirs(relativePath)
                    with open(iconFilePath, 'wb') as fp:
                        fp.write(f['body'])
                    data['file_name'] = filename
                    uploader = self.settings['uploader']
                    img_cdn_json = uploader.upload(iconFilePath, "png")

                    if not img_cdn_json or not img_cdn_json['url']:
                        data['status'] = self.UPLOAD_FAILED
                    else:
                        data['md5'] = str(img_cdn_json.get('md5'))
                        data['cdn_url'] = str(img_cdn_json.get('url'))
                        data['status'] = self.UPLOAD_SUCCESS
                    data['cdn_url'] = str('')
                    data['status'] = self.UPLOAD_SUCCESS
                except Exception as ex:
                    self._logger.error("Ajax: UploadIcon error:%s", str(ex), exc_info=1)
                    data['status'] = self.UPLOAD_FAILED
            else:
                data['status'] = self.UPLOAD_FAILED
        finally:
            self.json_result['data'] = data
            super(UploadImage, self).process_request()