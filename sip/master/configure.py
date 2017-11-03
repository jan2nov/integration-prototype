# coding: utf-8
"""A thread class run when the master controller is configured.

.. moduleauthor:: David Terrett
"""
import logging
import threading

from sip.master import slave_control
from sip.master.config import slave_config_dict


class Configure(threading.Thread):
    """Does the actual work of configuring the system."""

    def __init__(self):
        super(Configure, self).__init__()

    def run(self):
        """Thread run routine."""
        log = logging.getLogger(__name__)

        log.info('Starting configuration.')

        # Go through the slave map and start all the tasks that are marked
        # as being required for the system to be online. For these tasks
        # we use the same string for both the task name and type as, by
        # definition there is only one task of each type.
        for task, config in slave_config_dict().items():
            if config.get('online', False):
                slave_control.start(task, task)

        log.info('Configuration thread exiting.')
