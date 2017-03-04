#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Redis node task module.
"""

from rediscluster import StrictRedisCluster
import sys
import os
import signal

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from sip.common.logging_api import log


def _sig_handler(signum, frame):
    sys.exit(0)

def main():
    """Task run method."""
    # Install handler to respond to SIGTERM
    signal.signal(signal.SIGTERM, _sig_handler)
    sys.stdout.flush()
    print("inside the redis nodes")

    log.info("INSIDE REDIS NODE SCRIPT.........")
    startup_nodes = [{"host": "127.0.0.1", "port": "7000",
                      "host": "127.0.0.1", "port": "7001",
                      "host": "127.0.0.1", "port": "7002"
                      }]

    log.info("AFTER STARTUP NODE.........")
    # Note: decode_responses must be set to True when used with python3
    rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)

    # rc.set("telescope_model:sdp:pulsar_search:1:n_sub_integrations", "1000")
    # rc.set("telescope_model:sdp:pulsar_search:1:n_channels", "1001")
    # rc.set("telescope_model:sdp:pulsar_search:2:n_sub_integrations", "2000")
    # rc.set("telescope_model:sdp:pulsar_search:2:n_channels", "2001")

    # rc.set("telescope_model:sdp:pulsar_search:2:n_data", "100")
    #
    # rc.set("telescope_model:sdp:pulsar_search:1:test_data", "10")
    # rc.set("telescope_model:sdp:pulsar_search:2:test_data", "200")
    # rc.set("telescope_model:sdp:pulsar_search:1:more_test", "300")
    # rc.set("telescope_model:sdp:pulsar_search:2:more_test", "400")
    # rc.set("telescope_model:csp:pulsar_search:1:n_data", "500")
    # rc.set("telescope_model:csp:pulsar_search:2:n_data", "600")

    log.info("GETTING THE DATA")
    log.info(rc.get("telescope_model:sdp:pulsar_search:2:n_sub_integrations"))

    log.info("GETTING THE KEYS")
    log.info(rc.keys("telescope_model:csp:*"))

if __name__ == '__main__':
    main()

