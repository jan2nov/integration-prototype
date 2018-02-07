#!/usr/bin/python3

from redis_client import RedisDatabase as config
import redis


def test_config_database():
    # Connect to redis
    hostname = "localhost"
    port = 6379
    redis_api = config(hostname, port)

    # Testing the api
    data = redis_api.hget_all("ingest:visibility_receiver")
    print(data)


if __name__ == '__main__':
    test_config_database()
