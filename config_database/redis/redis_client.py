#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Redis node task module.
   Sets and queries data from redis database
"""

import redis


class RedisDatabase:

    def __init__(self):
        # Setting up connection with the master and a slave
        self._redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def get_variable(self, variable_name):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        response = my_server.get(variable_name)
        return response

    def get_keys(self, variable_name):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        response = my_server.keys(variable_name)
        return response

    def set_variable(self, variable_name, variable_value):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        my_server.set(variable_name, variable_value)

    def delete_variable(self, key):
        my_server = redis.Redis(connection_pool=self._redis_pool)
        my_server.delete(key)

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