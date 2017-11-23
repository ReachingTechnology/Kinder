# -*- coding: utf-8 -*-
#
import logging
import random
import msgpack
import heapq
import time

from flop.store.redispool import RedisConfig, RedisPool
from flop.utils.consistenthash import ConsistentHash
from redis.exceptions import ConnectionError

STATE_ONLINE = 1
STATE_OFFLINE = 0

DEFAULT_REPLICA_SET = 30

DEFAULT_CONSECUTIVE_FAIL_THROTTLE_TIME = 3600

REDIS_TIMEOUT = 3

RANDOM_RANGE_VALUE = 1024

class RedisProxy(object):
    
    class _ExpiredNodeItem(object):
        
        def __init__(self, node, pool, expiredTime):
            self.node = node
            self.pool = pool      
            self.expiredTime = expiredTime
                
        # Comparison methods to sort by nextTimeout, with object id as a tiebreaker
        # to guarantee a consistent ordering.  The heapq module uses __le__
        # in python2.5, and __lt__ in 2.6+ (sort() and most other comparisons
        # use __lt__).
        def __lt__(self, other):
            return ((self.expiredTime, id(self)) <
                    (other.expiredTime, id(other)))
    
        def __le__(self, other):
            return ((self.expiredTime, id(self)) <=
                    (other.expiredTime, id(other)))
            
        def __eq__(self, other):
            if isinstance(other, type(self.node)):
                return self.node == other
            else:
                return self.node == other.node
    
    class _RedisNode(object):
        
        def __init__(self, name, host, port, db, replicas, consecutive_fail_Time):
            if name:
                self.key = name
            else:
                self.key = "%s:%s" % (host, port)
            self.host = host
            self.port = port
            self.db = db
            self._failTimes = 0
            self._lastFailtime = 0
            self._replicas = replicas
            self._consecutive_fail_throttle_time = consecutive_fail_Time
            
        @property
        def replicas(self):
            return self._replicas
        
        def __str__(self):
            return self.key
        
        @property
        def fail_times(self):
            return self._failTimes
        
        def inc_fail_times(self):
            now = time.time()
            if (now - self._lastFailtime) <= self._consecutive_fail_throttle_time:
                self._failTimes += 1
            else:
                self._failTimes = 1            
            
        def set_last_fail_time(self):
            self._lastFailtime = time.time()        

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def initialize(self, clusterConfig, failTimeout = 100, sampleRate = 500):
        self._clusterConfig = clusterConfig
        self._failTimeout = failTimeout
        self._sampleRate = sampleRate
        self._sampleCount = 0
        self._masterRedisPool = None
        self._cohash = ConsistentHash()
        self._poolCluster = {}
        self._inactiveRedisPoolList = None
        self.refresh_redis_config()

    @property
    def master_pool(self):
        return self._masterRedisPool
    
    @property
    def cluster(self):
        return self._poolCluster.items()
        
    def _release_cluster_pool(self, cluster):
        for redisPool in cluster.itervalues():
            try:
                redisPool.close()
            except:
                pass
            
    def _init_event_redis_config(self, config):
        if self._masterRedisPool is None:
            masterConfig = RedisConfig(host=str(config['server']), 
                                       port=config['port'], 
                                       db=0)
            self._masterRedisPool = RedisPool(masterConfig)
        
    def refresh_redis_config(self):                    
        self._inactiveRedisPoolList = []
        for item in self._clusterConfig['cluster']:   
            redisNode = RedisProxy._RedisNode(item.get('name'),
                                              str(item['server']), 
                                              int(item['port']), 
                                              int(item['db']),
                                              int(item.get('replicas', DEFAULT_REPLICA_SET)),
                                              int(item.get('consecutive_fail_throttle_time', DEFAULT_CONSECUTIVE_FAIL_THROTTLE_TIME)))
                                    
            if not self._poolCluster.has_key(redisNode.key):
                redisConfig = RedisConfig(host=str(item['server']), 
                                          port=int(item['port']),
                                          db=int(item['db']),
                                          timeout=REDIS_TIMEOUT)
                self._poolCluster[redisNode.key] = RedisPool(redisConfig)
                self._cohash.add_node(redisNode, redisNode.replicas)
            self._logger.info("Configured redis: host[%s], port[%s], db[%s]", str(item['server']), int(item['port']), int(item['db']))

    def close(self):
        self._release_cluster_pool(self._poolCluster)
        
    def get_connection(self, key):
        if self._inactiveRedisPoolList:
            if self._sampleCount >= self._sampleRate:
                now = time.time()
                if self._inactiveRedisPoolList[0].expiredTime <= now:
                    expiredNodeItem = heapq.heappop(self._inactiveRedisPoolList)
                    redisNode = expiredNodeItem.node
                    redisNode.set_last_fail_time()
                    self._poolCluster[redisNode.key] = expiredNodeItem.pool
                    self._cohash.add_node(redisNode, redisNode.replicas)
            else:
                self._sampleCount += 1
        
        redisNode = self._cohash.get_node(key)
        redisPool = self._poolCluster.get(redisNode.key)
        return redisPool.get_connection(), redisNode
    
    def _handle_connection_error(self, redisNode):
        if redisNode is not None:
            redisNode.inc_fail_times()
            self._cohash.remove_node(redisNode, redisNode.replicas)
            redisPool = self._poolCluster[redisNode.key]        
            heapq.heappush(self._inactiveRedisPoolList, self._ExpiredNodeItem(redisNode, redisPool, int(time.time() + (redisNode.fail_times * self._failTimeout))))
            del self._poolCluster[redisNode.key]
            self._logger.error("Shutdown can't connected redis instance:%s", str(redisNode))
            
    def set_value_to_cache_bydb(self, key, value, expired, db, pack=False):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            pipeline.execute_command("select", db)
            if pack:
                packedValue = msgpack.packb(value)
                if expired != -1:
                    pipeline.setex(key, packedValue, expired)
                else:
                    pipeline.set(key, packedValue)
            else:
                if expired != -1:
                    pipeline.setex(key, value, expired)
                else:
                    pipeline.set(key, value)

            pipeline.execute_command("select", redisNode.db)
            pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Set key[%s] failed, due to connection time out", key, exc_info=1)
        except Exception:
            self._logger.error("Set key[%s] to redis cache failed", key, exc_info=1)            
    
    def set_value_to_cache(self, key, value, expired, pack=False):
        try:
            redisConn, redisNode = self.get_connection(key)
            if pack:
                packedValue = msgpack.packb(value)
                if expired != -1:
                    redisConn.setex(key, packedValue, expired)
                else:
                    redisConn.set(key, packedValue)
            else:
                if expired != -1:
                    redisConn.setex(key, value, expired)
                else:
                    redisConn.set(key, value)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Set key[%s] failed, due to connection time out", key, exc_info=1)
        except Exception:
            self._logger.error("Set key[%s] to redis cache failed", key, exc_info=1)
            
    def set_value_to_cache_by_random(self, randomKey, key, value, expired, pack=False):
        try:
            redisConn, redisNode = self.get_connection(randomKey)
            if pack:
                packedValue = msgpack.packb(value)
                if expired != -1:
                    redisConn.setex(key, packedValue, expired)
                else:
                    redisConn.set(key, packedValue)
            else:
                if expired != -1:
                    redisConn.setex(key, value, expired)
                else:
                    redisConn.set(key, value)                
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Set key[%s] failed, due to connection time out", key, exc_info=1)
        except Exception:
            self._logger.error("Set key[%s] to redis cache failed", key, exc_info=1)            
            
    def set_value_to_cache_by_hset(self, key, field, value, pack=False):
        try:
            redisConn, redisNode = self.get_connection(field)
            if pack:
                packedValue = msgpack.packb(value)
                redisConn.hset(key, field, packedValue)
            else:
                redisConn.hset(key, field, value)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Set key[%s] failed, due to connection time out", key, exc_info=1)  
        except Exception:
            self._logger.error("Set key[%s] to redis cache failed", key, exc_info=1)
            
    def set_value_to_cache_with_keyset(self, key, value, expired, pack, keyset):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            pipeline.sadd(keyset, key)
            if pack:
                packedValue = msgpack.packb(value)
                if expired != -1:
                    pipeline.setex(key, packedValue, expired)
                else:
                    pipeline.set(key, packedValue)                
            else:
                if expired != -1:
                    pipeline.setex(key, value, expired)
                else:
                    pipeline.set(key, value)
            pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Set key[%s] to redis cache with keyset[%s] failed, due to connection time out", key, keyset, exc_info=1)
        except Exception:
            self._logger.error("Set key[%s] to redis cache with keyset[%s] failed", key, keyset, exc_info=1)
            
    def get_value_from_redis_bydb(self, key, db, pack=False):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            pipeline.execute_command("select", db)
            pipeline.get(key)
            pipeline.execute_command("select", redisNode.db)
            result = pipeline.execute()
            packedData = result[1]
            if packedData is not None:
                if pack:
                    return msgpack.unpackb(packedData)
                else:
                    return packedData
            else:
                return None
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Get key[%s] failed, due to connection time out", key, exc_info=1)
            return None
        except Exception:
            self._logger.error("Get key[%s] value from redis cache failed", key, exc_info=1)
            return None                      
            
    def get_value_from_redis(self, key, pack=False):
        try:
            redisConn, redisNode = self.get_connection(key)
            packedData = redisConn.get(key)
            if packedData is not None:
                if pack:
                    return msgpack.unpackb(packedData)
                else:
                    return packedData
            else:
                return None
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Get key[%s] failed, due to connection time out", key, exc_info=1)
            return None
        except Exception:
            self._logger.error("Get key[%s] value from redis cache failed", key, exc_info=1)
            return None
        
    def get_value_from_redis_by_random(self, key, pack=False):
        try:
            randomKey = "%s:%s" % (key, random.randint(1, RANDOM_RANGE_VALUE))
            redisConn, redisNode = self.get_connection(randomKey)
            packedData = redisConn.get(key)
            if packedData is not None:
                if pack:
                    return msgpack.unpackb(packedData), randomKey
                else:
                    return packedData, randomKey
            else:
                return None, randomKey
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Get key[%s] failed, due to connection time out", key, exc_info=1)
            return None, randomKey
        except Exception:
            self._logger.error("Get key[%s] value from redis cache failed", key, exc_info=1)
            return None, randomKey   
        
    def get_value_from_cache_by_hset(self, key, field, pack=False):
        try:
            redisConn, redisNode = self.get_connection(field)
            packedData = redisConn.hget(key, field)
            if packedData is not None:
                if pack:
                    return msgpack.unpackb(packedData)
                else:
                    return packedData
            else:
                return None
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Get key[%s] failed, due to connection time out", key, exc_info=1)
            return None
        except Exception:
            self._logger.error("Get key[%s] to redis cache failed", key, exc_info=1)
            return None
        
    def get_and_delete_value_from_redis(self, key, pack=False):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            pipeline.get(key)
            pipeline.delete(key)
            result = pipeline.execute()
            if result[0] is not None:
                if pack:
                    return msgpack.unpackb(result[0])
                else:
                    return result[0]
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("GetAndDelete key[%s] failed, due to connection time out", key, exc_info=1)
            return None
        except Exception:
            self._logger.error("GetAndDelete key[%s] value from redis cache failed", key, exc_info=1)
            return None
        
    def delete_value_from_redis_bydb(self, key, db):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            pipeline.execute_command("select", db)
            pipeline.delete(key)
            pipeline.execute_command("select", redisNode.db)
            pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Delete key[%s] failed, due to connection time out", key, exc_info=1)         
        except Exception:
            self._logger.error("Delete key[%s] value from redis cache failed", key, exc_info=1)                      
        
    def delete_value_from_redis(self, key):
        try:
            redisConn, redisNode = self.get_connection(key)
            redisConn.delete(key)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Delete key[%s] failed, due to connection time out", key, exc_info=1)         
        except Exception:
            self._logger.error("Delete key[%s] value from redis cache failed", key, exc_info=1)            
        
    def delete_value_by_keys(self, keys):
        try:
            redisNode = None
            for key in keys:
                redisConn, redisNode = self.get_connection(key)
                redisConn.delete(key)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Delete keys[%s] failed, due to connection time out", str(keys), exc_info=1)    
        except Exception:
            self._logger.error("Delete keys[%s] value from redis cache failed", str(keys), exc_info=1)               
            
    def delete_value_by_keyset(self, keyset):
        try:
            redisNode = None
            for pool in self._redisPoolCluster.itervalues():
                redisConn, redisNode = pool.get_connection()
                cacheKeys =  redisConn.smembers(keyset)
                pipeline = redisConn.pipeline()
                for k in cacheKeys:
                    pipeline.delete(k)
                pipeline.delete(keyset)
                pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode) 
        except Exception:
            self._logger.error("Delete keyset[%s] value from redis cache failed", keyset, exc_info=1)
            
    def delete_value_from_cluster(self, key):
        try:
            redisNode = None
            for pool in self._redisPoolCluster.itervalues():
                redisConn, redisNode = pool.get_connection()
                redisConn.delete(key)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Delete key[%s] failed, due to connection time out", key, exc_info=1)
        except Exception:
            self._logger.error("Delete key[%s] value from all redis instance failed", key, exc_info=1)                        
        
    def flush_out_value_by_pattern(self, pattern):
        try:
            redisNode = None
            for pool in self._redisPoolCluster.itervalues():
                redisConn, redisNode = pool.get_connection()
                keys = redisConn.keys(pattern)
                pipeline = redisConn.pipeline()
                for key in keys:
                    pipeline.delete(key)
                pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("Flush pattern[%s] failed, due to connection time out", pattern, exc_info=1)
        except Exception:
            self._logger.error("Flush key pattern[%s] value from redis cache failed", pattern, exc_info=1)
            
    def create_rate_limit_value(self, key, expired):
        try:
            redisConn, redisNode = self.get_connection(key)
            value = redisConn.incr(key)
            if int(value) == 1:
                redisConn.expire(key, expired)
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("create rate limit key[%s] failed, due to connection time out", key, exc_info=1)
        except Exception:
            self._logger.error("create rate limit key[%s] failed", key, exc_info=1)
            
    def with_pipeline(self, key, *args):
        try:
            redisConn, redisNode = self.get_connection(key)
            pipeline = redisConn.pipeline()
            for func in args:
                func(pipeline)
            return pipeline.execute()
        except ConnectionError:
            self._handle_connection_error(redisNode)
            self._logger.error("create rate limit key[%s] failed, due to connection time out", key, exc_info=1)
            return None
        except Exception:
            self._logger.error("create rate limit key[%s] failed", key, exc_info=1)
            return None                                  