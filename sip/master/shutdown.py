# coding: utf-8
"""Functions executed when the master controller is shut down.

.. moduleauthor:: David Terrett
"""
import logging
import os
import threading
import time

from sip.master import config, slave_control
from sip.master.config import slave_status_dict


class Shutdown(threading.Thread):
    """Does the actual work of shutting down the system."""

    def __init__(self):
        super(Shutdown, self).__init__()

    def run(self):
        """Thread run routine."""
        log = logging.getLogger(__name__)
        log.info('starting shutdown')

        # Shut down any slaves that are still running
        for slave, status in slave_status_dict().items():
            state = status['state'].current_state()
            print(state)
            if state != 'Exited' and state != 'Unknown':
                slave_control.stop(slave, status)

        # Shut down the log server
        log.info('Terminating logging server: %s', config.logserver.ident)
        try:
            print(config.logserver.status())

            config.logserver.delete()
        except RuntimeError:
            log.warning('Unable to terminate logging server.')

        print('Shutdown complete. Goodbye!')

        # Give the rpc service a chance to send a reply
        time.sleep(1)
        os._exit(0)
