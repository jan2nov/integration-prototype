# coding: utf-8
"""Module which provides a function which tries to reconnect to running
services
"""
import logging

from sip.master.config import slave_config_dict
from sip.master import slave_control


def reconnect(paas):
    """Function that tries to reconnect to running services."""
    log = logging.getLogger(__name__)
    # Go through all the "online" services in the slave map see if
    # the corresponding service is running
    for name, config in slave_config_dict().items():
        if config['online']:

            # Try to get a descriptor for the service
            try:
                log.info('Attempting to reconnect to {}'.format(name))
                descriptor = paas.find_task(name)
                slave_control.reconnect(name, descriptor)
            except RuntimeError as error:
                if 'not found' in error.args[0]:
                    log.warning('Reconnection to "%s" service failed.: '
                                'Service not found.', name)
                    continue
                raise
