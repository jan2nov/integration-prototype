# Docker Redis Cluster

Docker image with redis built and installed from source. The main usage
for this container is to test redis cluster code. The cluster is 6 redis
instances running with 3 master & 3 slaves, one slave for each master.
They run on ports 7000 to 7005.It also contains 2 standalone instances
that is not part of the cluster. They are running on port 7006 & 7007.
This image requires at least `Docker` version 1.10 but the latest version is recommended.

Install Redis

    wget http://download.redis.io/releases/redis-3.2.6.tar.gz
    tar xzf redis-3.2.6.tar.gz
    cd redis-3.2.6
    make

Redis for Python

    sudo pip3 install redis
    sudo pip3 install redis-py-cluster

Build Docker

To build your own image run:

    cd sip/redis-cluster

    make build

To run the container use:

    make run

To stop the container run

    make stop

To connect to your cluster you can use the redis-cli tool:

    redis-cli -c -p 7000

    execute commands such as

    SET mykey HELLO
    SET foo bar
    GET mykey
    GET foo
    keys *

    You should be able to see that redis cluster nodes are able to redirect a client
    to the right node.

    or

    execute python3 -m sample_data.py

    This will set and get data from redis using redis python client.
