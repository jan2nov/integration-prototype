# coding: utf-8
"""Functions executed when the master controller is shut down."""

__author__ = 'David Terrett'

import os
import signal
import threading
import time
import subprocess

from sip.common.logging_api import log

from sip.master import config
from sip.master import slave_control


class Shutdown(threading.Thread):
    """Does the actual work of shutting down the system."""

    def __init__(self):
        super(Shutdown, self).__init__()

    def run(self):
        """Thread run routine."""
        log.info('starting shutdown')

        # Shut down any slaves that are still running
        for slave, status in config.slave_status.items():
            if status['state'].current_state() != '_End':
                slave_control.stop(slave, status)

        # Shut down the log server
        log.info('Terminating logserver, pid ', config.logserver.pid)
        config.logserver.send_signal(signal.SIGINT)
        # os.kill(config.logserver.pid, signal.SIGTERM)

        # # Stopping redis-server with redis-cli (instead of just killing it)
        # print("Stopping redis-server... ")
        # command = '/home/njthykkathu/redis-3.2.6/src/redis-cli -p 6379 shutdown'
        # subprocess.Popen(command.split(), shell=False)

        # Stopping redis cluster (instead of just killing it)
        print("Stopping redis cluster... ")
        command = '/home/njthykkathu/cluster-test/create-cluster stop'
        subprocess.Popen(command.split(), shell=False)

        print('Shutdown complete. Goodbye!')

        # Give the rpc service a chance to send a reply
        time.sleep(1)
        os._exit(0)
