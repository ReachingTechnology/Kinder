#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import os
import time
import urllib2
import ujson

from datetime import datetime

from backend.conf.config import SystemConfig
from backend.handler.async_handler import AsynchronousHandler
from backend.handler.util.Util import Util
from backend.handler.util.DateUtil import DateUtil


class DocumentHandler(AsynchronousHandler):
    UPLOAD_SUCCESS = 0
    UPLOAD_FAILED = -1
    UPLOAD_DONT_MATCH_REQUIRE = -2

    def initialize(self, op):
        self._op = op
        self._document_info_coll = self.settings['kinder_mongo_pool'].get_collection('kinder', "document_info")

    def process_request(self):
        if self._op == 'get_document_list':
            arguments = ujson.loads(self.request.body)
            queryLevel = arguments['level']
            docs = self._document_info_coll.find({'level': queryLevel})
            self.json_result = docs
        elif self._op == 'upload_document_country' or self._op == 'upload_document_city' or self._op == 'upload_document_kindergarten':
            try:
                self.json_result = {}
                data = {}
                if self.request.files:
                    # file_para = self.get_arguments('input_name', [])[0]
                    f = self.request.files['file'][0]
                    try:
                        resp = {}
                        filename = f["filename"]
                        fileSize = len(f['body'])
                        params = self.request.arguments
                        root, ext = os.path.splitext(filename)
                        current_time_str = str(time.time())
                        transition_filename = Util.get_str_md5(current_time_str + filename) + ext
                        now = datetime.now()
                        # self._logger.info(self.settings['img_upload_path'])
                        level = 'KINDERGARTEN'
                        if self._op == 'upload_document_country':
                            level = 'COUNTRY'
                        elif self._op == 'upload_document_city':
                            level = 'PROV&CITY'
                        relativePath = os.sep.join(
                            (self.settings['img_upload_path'], 'documents', level))
                        iconFilePath = os.sep.join((relativePath, transition_filename))  # 完整路径
                        # self._logger.info(iconFilePath)
                        if not os.path.exists(relativePath):
                            os.makedirs(relativePath)
                        with open(iconFilePath, 'wb') as fp:
                            fp.write(f['body'])

                        basePath = self.settings['base_path']
                        data['fileurl'] = iconFilePath[len(basePath):]
                        # uploader = self.settings['uploader']
                        # img_cdn_json = uploader.upload(iconFilePath, "png")
                        #
                        # if not img_cdn_json or not img_cdn_json['url']:
                        #     data['status'] = self.UPLOAD_FAILED
                        # else:
                        #     data['md5'] = str(img_cdn_json.get('md5'))
                        #     data['cdn_url'] = str(img_cdn_json.get('url'))
                        #     data['status'] = self.UPLOAD_SUCCESS
                        # data['cdn_url'] = str('')

                        existFiles = self._document_info_coll.find().sort("_id", -1)
                        fileEntry = {}
                        
                        existCount = existFiles.count()
                        if existCount == 0:
                            newid = "FILE_00000001"
                            newseq = 1
                        else:
                            lastFile = existFiles.next()
                            newseq = lastFile['seq'] + 1
                            newid = "FILE_{:0>8d}".format(newseq)
                        fileEntry['_id'] = newid
                        fileEntry['seq'] = newseq
                            
                        fileEntry['name'] = filename
                        fileEntry['url'] = data['fileurl']
                        fileEntry['level'] = level
                        fileEntry['upload_time'] = DateUtil.get_current_time()
                        fileEntry['uploader'] = params['uploader'][0]
                        fileEntry['size'] = fileSize
                        self._document_info_coll.save(fileEntry)

                        data['status'] = self.UPLOAD_SUCCESS
                    except Exception as ex:
                        # self._logger.error("Ajax: UploadIcon error:%s", str(ex), exc_info=1)
                        data['status'] = self.UPLOAD_FAILED
                else:
                    data['status'] = self.UPLOAD_FAILED
            finally:
                self.json_result['data'] = data
        elif self._op == 'remove_document':
            arguments = ujson.loads(self.request.body)
            id = arguments['id']
            file = self._document_info_coll.find_one({'_id': id})
            if file != None:
                basePath = self.settings['base_path']
                filePath = basePath + file['url']
                os.remove(filePath)
                self._document_info_coll.remove({'_id': id})
            self.json_result = {'status': 0}
        super(DocumentHandler, self).process_request()


