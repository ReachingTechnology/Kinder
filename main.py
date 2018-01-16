#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 Zhang Hao
#

import logging
import os
import signal
import sys
# import uuid
# import base64
import time

# tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
# ---- flop library ----
from flop.pool.threadpool import ThreadManager
from flop.pool.timer import TimerWorker
from flop.store.mongoaccount import MongoAccount
from flop.store.mongopool import MongoPool
from flop.utils.utilities import Util
from tornado.options import define, options

# --- database ----
from backend.conf.config import SystemConfig

# --- request handlers ---
from urls import URLS

# # --- util ---
from backend.common.redisproxy import RedisProxy
from backend.common.userManager import UserManager

reload(sys)
sys.setdefaultencoding('utf8')

# define listen port
define("port", default=7070, help="run on the given port", type=int)
define("conf", default="./backend/conf/settings.json", help="configuration file", type=str)

# define configuration
ConfigSettings = {}
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5


class KinderApplication(tornado.web.Application):
    def __init__(self):
        settings = {
            "domain": SystemConfig.domain,
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "backend/template"),
            "img_upload_path": os.path.join(os.path.dirname(__file__), 'static', 'upload'),
            "cookie_secret": "4K1sh0zAQi6PxgfQpDys7UHnVXTX205Xmvp347o33Lc=",
        # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            "xsrf_cookies": False,
            "login_url": "/login",
            "system_name": "",
            "debug": SystemConfig.debug,  # changeTo False if online
            "listen_info": ConfigSettings['listen_info'],
            "redis_proxy": ConfigSettings['redis_proxy'],
            "thread_pool": ConfigSettings['thread_pool'],
            "kinder_mongo_pool": ConfigSettings['kinder_mongo_pool'],
            "timer": ConfigSettings['timer'],
            # "uploader": ConfigSettings['uploader'],
            # "rolelist": ConfigSettings['rolelist'],

        }
        handlers = URLS
        # handlers.append((r"/static/(.*)", tornado.web.StaticFileHandler, dict(path=settings['static_path'])))
        handlers.append((r"/(.*)", tornado.web.StaticFileHandler, dict(default_filename='index.html', path=os.path.dirname(__file__))))
        tornado.web.Application.__init__(self, handlers, **settings)


def initialize_server():
    init_connection_pool()

    # initialize thread pool
    threadPool = ThreadManager()
    threadPool.initialize()
    ConfigSettings['thread_pool'] = threadPool

    # initialize timer
    timer = TimerWorker()
    timer.initialize(threadPool)
    ConfigSettings['timer'] = timer

    # ConfigSettings['uploader'] = UploadEngine(SystemConfig.mfs_url)
    #
    UserManager.instance().initialize(ConfigSettings['redis_proxy'])
    # init_role_list()


def init_connection_pool():

    kinder_mongo_conf = SystemConfig.kinder_mongo
    kinder_mongo_account = MongoAccount(kinder_mongo_conf["db_user"],
                                        kinder_mongo_conf["db_pass"],
                                        kinder_mongo_conf["db_sock"],
                                        kinder_mongo_conf["db_size"])
    kinder_mongo_pool = MongoPool()
    kinder_mongo_pool.connect(kinder_mongo_account)
    ConfigSettings['kinder_mongo_pool'] = kinder_mongo_pool

    # initialize redis pools
    clusterConfig = SystemConfig.redis_data
    redisProxy = RedisProxy()
    redisProxy.initialize(clusterConfig)
    ConfigSettings['redis_proxy'] = redisProxy

    # initialize mysql
    # mysqlConf = SystemConfig.mysql
    # mysqlaccount = MysqlAccount(mysqlConf["db_host"],
    #                             mysqlConf["db_user"],
    #                             mysqlConf["db_pass"],
    #                             mysqlConf["db_base"],
    #                             mysqlConf["db_sock"],
    #                             mysqlConf["db_port"])
    # mysqlPool = MysqlConnectionPool()
    # mysqlPool.initialize(mysqlaccount, mysqlConf["pool_size"])
    # ConfigSettings['mysql_pool'] = mysqlPool


def init_config(config_file):
    SystemConfig.load_setting_json(config_file)


def init_role_list():
    rolelist = []
    conn = ConfigSettings['mysql_pool'].get_connection()
    try:
        conn.execute("SELECT id,name from t_cms_role")
        conn.commit()
        roles = conn.rows()
    finally:
        ConfigSettings['mysql_pool'].free_connection(conn)
    for role in roles:
        rolelist.append(role)
    ConfigSettings['rolelist'] = rolelist


def shutdown_server():
    ConfigSettings['timer'].stop()
    ConfigSettings['thread_pool'].stop()
    ConfigSettings['mysql_pool'].close()
    ConfigSettings['mongo_pool'].disconnect()
    ConfigSettings['redis_listener'].stop()


def sig_handler(sig, frame):
    logging.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    logging.info('Stopping http server')
    ConfigSettings['http_server'].stop()

    logging.info('Will shutdown in %s seconds ...', MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()

    stop_loop()


def main():
    options.log_to_stderr = False
    tornado.options.parse_command_line()
    config_file = options.conf
    init_config(config_file)

    log_level = logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)

    formatter = logging.Formatter('[%(asctime)s][module:%(module)s][line:%(lineno)d][%(levelname)s]: %(message)s')
    log_FileHandler = logging.handlers.TimedRotatingFileHandler(filename=SystemConfig.logfile,
                                                                when='D',
                                                                interval=1,
                                                                backupCount=3)

    log_FileHandler.setFormatter(formatter)
    log_FileHandler.setLevel(log_level)
    logger.addHandler(log_FileHandler)

    ##write log into console
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    SystemConfig.init_logger()

    logger.info("=======================================================================")
    logger.info("start to launch misc cms service....")

    initialize_server()
    ipAddr = Util.get_ip_address("eth0")
    logger.info("Listen info ip:%s, port:%s", ipAddr, options.port)
    ConfigSettings['listen_info'] = {'host': ipAddr, 'port': options.port}

    http_server = tornado.httpserver.HTTPServer(KinderApplication(), ssl_options={
        "certfile": os.path.join(os.path.dirname(__file__), "backend/secure/server.crt"),
        "keyfile": os.path.join(os.path.dirname(__file__), "backend/secure/server.key"),
    })
    http_server.listen(options.port)
    # http_server.listen(options.port, address='0.0.0.0')
    ConfigSettings['http_server'] = http_server
    # add signal handler
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    logger.info("misc cms start on port %s completed." % options.port)
    print "misc cms start on port %s completed." % options.port
    tornado.ioloop.IOLoop.instance().start()
    shutdown_server()  # shutdown server


if __name__ == "__main__":
    main()