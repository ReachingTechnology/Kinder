#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime
import ujson
import tornado.web
import tornado.ioloop
import backend.handler.base


class AsynchronousHandler(backend.handler.base.BaseHandler):
    '''
    Asynchronous base handler
    '''

    @tornado.web.asynchronous
    def handle(self):
        self.json_result = {}
        try:
            self.settings['thread_pool'].add_task(self.process_request, callback=None)
        except Exception as ex:
            self._logger.error("Cann't add task to thread pool, due to :%s", ex, exc_info=1)
            self.send_response()

    def _get_timeline(self, latestDays):
        if latestDays >= 0:
            now = datetime.date.today()
            dayDelta = datetime.timedelta(days=latestDays)
            return (now - dayDelta)
        else:
            return None

    def _get_limit_condition(self, pageNo, pageSize):
        if pageNo >= 1:
            offset = (pageNo - 1) * pageSize
            return ''.join((" limit ", str(offset), ",", str(pageSize)))
        else:
            return None

    def process_request(self):
        # dummy implementation, all sub-handler should implement this function
        if self.get_status() == 200:
            self.json_result = ujson.dumps(self.json_result, ensure_ascii=False)
            self.write(self.json_result)
        tornado.ioloop.IOLoop.instance().add_callback(self.send_response)

    def _async_complete(self, jsonData):
        if self.get_status() == 200:
            self.write(ujson.dumps(jsonData, ensure_ascii=False))
        tornado.ioloop.IOLoop.instance().add_callback(self.send_response)

    def send_response(self):
        if self.get_status() == 200:
            self.finish()
        else:
            self.write_error(self.get_status())

