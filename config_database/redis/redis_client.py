#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Redis node task module.
   Sets and queries data from redis database
"""

import redis

class RedisDatabase:

    def __init__(self, hostname, port):
        # Setting up connection with the master and a slave
        self._redis_pool = redis.ConnectionPool(host=hostname, port=port, db=0)
        self._server = redis.Redis(connection_pool=self._redis_pool)

    def get_variable(self, variable_name):
        resp = self._server.get(variable_name)
        format_resp = int(resp)
        return format_resp 

    def get_keys(self, variable_name):
        resp = self._server.keys(variable_name)
        return resp

    def set_variable(self, variable_name, variable_value):
        self._server.set(variable_name, variable_value)

    def delete_variable(self, key):
        self._server.delete(key)

    def hmset_variable(self, variable_name, value):
        resp = self._server.hmset(variable_name, value)

    def hget_all(self, var):
        resp = self._server.hgetall(var)
        return resp

    def hget_variable(self,var, port):
        resp = self._server.hget(var, port)
        format_resp = int(resp)
        return format_resp
