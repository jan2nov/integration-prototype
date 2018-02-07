#!/usr/bin/python3

from redis_client import RedisDatabase as config
import redis


def test_config_database():
    # Connect to redis
    hostname = "localhost"
    port = 6379
    redis_api = config(hostname, port)

    # Testing the api
    initial = redis_api.get_variable("memory_pool:initial")
    print(initial)
    data = redis_api.hget_all("stream")
    for test in data:
        port_value = redis_api.hget_variable("stream", test.decode('utf-8'))
        print(port_value)


if __name__ == '__main__':
    test_config_database()
