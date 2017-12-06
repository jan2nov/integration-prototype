#!/usr/bin/python3

from redis_client import RedisDatabase as config


def main():
    """Task run method."""
    # Setting data to the database
    redis_api = config()
    redis_api.set_variable("output:max_times_per_file", "4")

    get = redis_api.get_variable('output:max_times_per_file')
    print(get)

if __name__ == '__main__':
    main()
