# coding: utf-8
"""Functions executed when the master controller is un-configured."""

__author__ = 'David Terrett'

import threading

from sip.common.logging_api import log
from sip.master import config


class UnConfigure(threading.Thread):
    """Does the actual work of un-configuring the system.

    Unloads all the loaded tasks
    """
    def __init__(self):
        super(UnConfigure, self).__init__()

    def run(self):
        """Thread run routine."""
        log.info('starting unconfiguration')
        for slave, status in config.slave_status.items():
            if status['state'].current_state() == 'Running':
                log.info('stopping {}'.format(slave))
                status['task_controller'].stop()
                status['descriptor'].delete()
        log.info('unconfigure done')
