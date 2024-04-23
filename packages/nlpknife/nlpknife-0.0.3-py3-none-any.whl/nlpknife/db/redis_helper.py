'''
Description: Redis
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 11:26:27
LastEditTime: 2024-01-04 11:26:31
'''
import redis 
import json

class RedisHelper:
    def __init__(self,host,port):
        self._pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
        self._r = redis.Redis(connection_pool=self._pool)
    
    def insert_data(self,key,value):
        self._r.set(key, value)

    def exists(self,key):
        return self._r.exists(key)

    def get_data(self,key):
        if self.exists(key):
            value = self._r.get(key)
        else:
            value = None
        return value
        
