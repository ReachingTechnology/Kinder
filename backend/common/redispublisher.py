# -*- coding: utf-8 -*-
#

import logging
import threading
import Queue

from threading import Thread
from flop.store.redispool import RedisConfig, RedisPool

class RedisPublish(Thread):
    
    PUBLISH_THREAD_NAME = "RedisPublisher"

    def __init__(self):
        threading.Thread.__init__(self, name=self.PUBLISH_THREAD_NAME)
        self._logger = logging.getLogger(self.__class__.__name__)        
        self._eventQueue = Queue.Queue()
        
    def initialize(self, config):        
        redisConfig = RedisConfig(host=str(config['server']), 
                                  port=config['port'],
                                  db=config['db'])
        self._redisPool = RedisPool(redisConfig)
        self.start()
        
    def publish_event(self, channel, data):
        self._eventQueue.put((channel, data))
        
    def run(self):
        self._logger.info("Relay publisher start to work...")
        while 1:
            try:
                channel, data = self._eventQueue.get()
                self._send_event(channel, data)
            except Exception as ex:
                self._logger.error("Get redis event [%s] [%s]  from queue failed, due to: %s", channel, data, str(ex), exc_info=1)        
        
    def _send_event(self, channel, data):    
        try:
            redisConn = self._redisPool.get_connection()
            redisConn.publish(channel, data)
            self._logger.info("Publish redis event: %s %s", channel, data)
        except Exception as ex:
            self._logger.error("Publish %s redis event occur exception:%s", str(ex), exc_info=1)