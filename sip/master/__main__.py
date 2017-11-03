# -*- coding: utf-8 -*-
"""Master controller main program.

.. moduleauthor:: David Terret
.. moduleauthor:: Brian McIlwrath
"""

import json
import logging
import logging.handlers
import logging.config
import os
import threading
import time

import requests
from rpyc.utils.server import ThreadedServer

# Export environment variable SIP_HOSTNAME
# This is needed before the other SIP imports.
os.environ['SIP_HOSTNAME'] = os.uname()[1]

from sip.common.resource_manager import ResourceManager
from sip.common.docker_paas import DockerPaas as Paas
from sip.master import config
from sip.zmq_logging_handler.zmq_logging_handler import ZmqLogHandler


def attach_zmq_handler(hosts=None):
    """ Attach a ZMQ logging handler.

    Args:
        hosts (list of str): List of hosts to attempt to connect to.
    """
    log = logging.getLogger(__name__)
    if not hosts:
        hosts = ['localhost', 'zla']
    for host in hosts:
        log.debug('Trying to connect to log aggregator on host %s', host)
        try:
            # TODO may need to wait until the logging server is up before
            # connecting (timeout setting waiting to connect to the healthcheck
            # api)
            handler = ZmqLogHandler(host=host)
            log.debug('Connected to log aggregator on host %s', host)
            log.addHandler(handler)
            break
        except requests.exceptions.ConnectionError:
            log.warning('Unable to connect to logging aggregator on '
                        'host %s', host)


def main():
    """ Main function.
    """
    log = logging.getLogger(__name__)

    log.debug('Starting ZMQ Logging aggregator service')
    # Start logging aggregator service.
    paas = Paas()
    # config.logserver = paas.run_service(
    #     'logging_server', 'sip',
    #     [logging.handlers.DEFAULT_TCP_LOGGING_PORT],
    #     ['python3', 'sip/common/logging_server.py'])
    health_check_port = 5555
    config.logserver = paas.run_service(
        'zla', 'sip', [logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                       logging.config.DEFAULT_LOGGING_CONFIG_PORT,
                       health_check_port],
        ['python3', '-m', 'sip.zmq_logging_aggregator'])
    # TODO(BM) use the task status (config.logserver.status()) to make sure the
    # service is running

    # Wait for the health check to report that it is up and running correctly.

    # FIXME(BM) remove this
    return

    # hostname = 'zla'
    # health_check_port = 5555
    # health_check_timeout = 5.0
    # health_check_url = ('http://{}:{}/healthcheck'.
    #                     format(hostname, health_check_port))
    # response = requests.get(health_check_url, timeout=health_check_timeout)
    # health_state = response.json()
    # if health_state['module'] != 'zmq_logging_aggregator':
    #     raise RuntimeError('Logging aggregator does not exist')

    # Attach the ZMQ handler to the logger.
    attach_zmq_handler(hosts=['zla'])

    # Define paths for static configuration files.
    sip_root = os.path.join(os.path.dirname(__file__), '..')
    config_file = os.path.join(sip_root, 'etc', 'slave_map.json')
    resources_file = os.path.join(sip_root, 'etc', 'resources.json')

    # Create the resource manager
    log.debug('Creating resource manager.')
    with open(resources_file) as f:
        _resources = json.load(f)
        if 'localhost' in _resources:
            _resources['localhost']['sip_root'] = sip_root
        log.debug('Resources:')
        for i, resource in enumerate(_resources):
            log.debug('[%03d] %s', i, resource)
            for key, value in _resources[resource].items():
                log.debug('  - %s %s', key, value)
        config.resource = ResourceManager(_resources)

    # FIXME(BM) do these have to be here... ?
    # -- not if it was due to logging.
    from sip.master.master_states import MasterControllerSM
    from sip.master.slave_poller import SlavePoller
    from sip.master.rpc_service import RpcService
    from sip.master.reconnect import reconnect

    # Create the slave config array from the configuration (a JSON string)
    with open(config_file) as f:
        config._slave_config_dict = json.load(f)

    # Create the master controller state machine
    config.master_controller_state_machine = MasterControllerSM()

    # Create and start the slave poller
    SlavePoller(config.master_controller_state_machine).start()

    # This starts the rpyc 'ThreadedServer' - this creates a new
    # thread for each connection on the given port
    server = ThreadedServer(RpcService, port=12345)
    t = threading.Thread(target=server.start)
    t.setDaemon(True)
    t.start()

    # Attempt to connect to exiting services
    reconnect(paas)

    # For testing we can also post events typed on the terminal
    log.debug('Starting the CLI')
    sm = config.master_controller_state_machine
    while True:
        if os.path.exists("docker_swarm"):
            time.sleep(1)
        else:
            # Read from the terminal and process the event
            event = input('** Enter command: ').split()
            if event:
                if event[0] == 'state':
                    log.info('CLI: Current state: {}'.
                             format(sm.current_state()))
                    continue
                log.info('CLI: !!! Posting event ==> {}'.format(event[0]))
                result = sm.post_event(event)
                if result == 'rejected':
                    log.warning('CLI: not allowed in current state')
                elif result == 'ignored':
                    log.warning('CLI: command ignored: {}'.format(event[0]))
                else:
                    # Print what state we are now in.
                    log.info('CLI: master controller state: {}'.format(
                        sm.current_state()))
            else:
                print('** Allowed commands: online, offline, shutdown, '
                      'cap [name] [task]')


if __name__ == '__main__':

    # Set up local logging.
    DOCKER_LOGS = logging.getLogger('docker')
    DOCKER_LOGS.propagate = False

    DOCKER_LOGS = logging.getLogger('RPC/12345')
    DOCKER_LOGS.propagate = False

    DOCKER_LOGS = logging.getLogger('urllib3')
    DOCKER_LOGS.propagate = False

    LOG = logging.getLogger('')
    FORMATTER = logging.Formatter("= [%(levelname).1s] %(message)-60s "
                                  "(%(name)s)")
    HANDLER = logging.StreamHandler()
    HANDLER.setFormatter(FORMATTER)
    LOG.addHandler(HANDLER)
    LOG.setLevel(logging.DEBUG)

    # Start the service.
    main()
