#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Redis node task module.
   Sets and queries data from redis database
"""

from rediscluster import StrictRedisCluster


def main():
    """Task run method."""

    # Starting up redis nodes
    startup_nodes = [{"host": "127.0.0.1", "port": "7000",
                      "host": "127.0.0.1", "port": "7001",
                      "host": "127.0.0.1", "port": "7002"
                      }]

    # Note: decode_responses must be set to True when used with python3
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    # Sets Data in Redis Database
    rc.set("telescope_model:sdp:pulsar_search:1:n_sub_integrations", "1000")
    rc.set("telescope_model:sdp:pulsar_search:1:n_channels", "1001")
    rc.set("telescope_model:sdp:pulsar_search:2:n_sub_integrations", "2000")
    rc.set("telescope_model:sdp:pulsar_search:2:n_channels", "2001")
    rc.set("telescope_model:sdp:pulsar_search:2:n_data", "100")
    rc.set("telescope_model:sdp:pulsar_search:1:test_data", "10")
    rc.set("telescope_model:sdp:pulsar_search:2:test_data", "200")
    rc.set("telescope_model:sdp:pulsar_search:1:more_test", "300")
    rc.set("telescope_model:sdp:pulsar_search:2:more_test", "400")
    rc.set("telescope_model:csp:pulsar_search:1:n_data", "500")
    rc.set("telescope_model:csp:pulsar_search:2:n_data", "600")

    # Querying data from the database
    print(rc.get("telescope_model:sdp:pulsar_search:2:n_sub_integrations"))

    # Querying keys from the database
    print(rc.keys("telescope_model:csp:*"))

if __name__ == '__main__':
    main()



