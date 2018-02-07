#!/usr/bin/python3

from redis_client import RedisDatabase as config
# import subprocess
import redis


def main():
    """Task run method."""
    # Start the server
    # command = "redis-server /etc/redis/redis.conf"
    # subprocess.call(command.split())

    # Connect to redis
    hostname = "localhost"
    port = 6379
    redis_api = config(hostname, port)
    
    # Defaults
    port = {'port': '8001'}

    print("Configuration Loading Started")

    # Visibility Receiver Config
    # redis_api.hmset_variable("ingest:visibility_receiver",
    #                          {'online': '0', 'timeout': '10'})
    # redis_api.hmset_variable("ingest:visibility_receiver:memory_pool",
    #                          {'lower': '16384', 'upper': '26214400',
    #                           'max_free': '12', 'initial': '8'})
    # redis_api.hmset_variable("stream", port)
    redis_api.hmset_variable("ingest:visibility_receiver",
                             {'output:max_times_per_file': '4',
                              'memory_pool:lower': '16384',
                              'memory_pool:upper': '26214400',
                              'memory_pool:max_free': '12',
                              'memory_pool:initial': '8', 'stream': port})
    redis_api.hmset_variable("stream", port)







    # Pulsar Receiver Config
    # redis_api.set_variable("output:max_times_per_file", "4")
    # redis_api.set_variable("memory_pool:lower", "16384")
    # redis_api.set_variable("memory_pool:upper", "26214400")
    # redis_api.set_variable("memory_pool:max_free", "12")
    # redis_api.set_variable("memory_pool:initial", "8")
    print("Visibility Receiver Configuration Loading Done")


if __name__ == '__main__':
    main()
