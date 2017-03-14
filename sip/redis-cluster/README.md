Docker Redis Cluster

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

Build Docker

To build your own image run:

    cd sip/redis-cluster

    make build

And to run the container use:

    make run

    # and top stop the container run

    make stop

To connect to your cluster you can use the redis-cli tool:

    redis-cli -c -p 7000


For testing
