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
    port = {"port":"8001"}

    print("Configuration Loading Started")

    # Visibility Receiver Config
    redis_api.set_variable("output:max_times_per_file", "4")
    redis_api.set_variable("memory_pool:lower", "16384")
    redis_api.set_variable("memory_pool:upper", "26214400")
    redis_api.set_variable("memory_pool:max_free", "12")
    redis_api.set_variable("memory_pool:initial", "8")
    redis_api.hmset_variable("stream", port)

    print("Visibility Receiver configuration Loading Done")

    # Testing the api
    initial = redis_api.get_variable("memory_pool:initial")
    # print(initial)
    data = redis_api.hget_all("stream")
    for test in data:
        port_value = redis_api.hget_variable("stream", test.decode('utf-8'))
        # print(port_value)

if __name__ == '__main__':
    main()
