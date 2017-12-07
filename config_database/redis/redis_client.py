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

    def get_variable(self, variable_name):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        resp = my_server.get(variable_name)
        format_resp = int(resp)
        return format_resp 

    def get_keys(self, variable_name):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        resp = my_server.keys(variable_name)
        return resp

    def set_variable(self, variable_name, variable_value):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        my_server.set(variable_name, variable_value)

    def delete_variable(self, key):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        my_server.delete(key)

    def hmset_variable(self, variable_name, value):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        resp = my_server.hmset(variable_name, value)

    def hget_all(self, var):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        resp = my_server.hgetall(var)
        return resp

    def hget_variable(self,var, port):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        resp = my_server.hget(var, port)
        format_resp = int(resp)
        return format_resp 


#
# def main():
#     """Task run method."""
#     # Setting data to the database
#     set_variable("foo", "bar")
#     set_variable("telescope_model:sdp:pulsar_search:1:n_sub_integrations", "1000")
#     set_variable("telescope_model:sdp:pulsar_search:1:n_channels", "1001")
#     set_variable("telescope_model:sdp:pulsar_search:2:n_sub_integrations", "2000")
#     set_variable("telescope_model:sdp:pulsar_search:2:n_channels", "2001")
#     set_variable("telescope_model:sdp:pulsar_search:2:n_data", "100")
#     set_variable("telescope_model:sdp:pulsar_search:1:test_data", "10")
#     set_variable("telescope_model:sdp:pulsar_search:2:test_data", "200")
#     set_variable("telescope_model:csp:pulsar_search:1:n_data", "500")
#     set_variable("telescope_model:csp:pulsar_search:2:n_data", "600")
#
#     # Querying data from the redis database
#     sub_int = get_variable('telescope_model:sdp:pulsar_search:2:n_sub_integrations')
#     print("SUB INT - " + str(sub_int))
#     n_data = get_variable('telescope_model:csp:pulsar_search:1:n_data')
#     print("N_DATA - " + str(n_data))
#
#     # Get keys from the database
#     keys = get_keys('telescope_model:csp*')
#     print("KEYS - " + str(keys))
#
#     # Delete a key
#     delete_variable('foo')
#
# if __name__ == '__main__':
#     main()
