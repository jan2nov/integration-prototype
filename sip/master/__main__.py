# -*- coding: utf-8 -*-
"""Master controller main program.

.. moduleauthor:: David Terret
.. moduleauthor:: Brian McIlwrath
.. moduleauthor:: Ben Mort
"""

import json
import logging
import logging.handlers
import logging.config
import os
import threading
import time
# import readline

from rpyc.utils.server import ThreadedServer

# Export environment variable SIP_HOSTNAME
# This is needed before the other SIP imports.
os.environ['SIP_HOSTNAME'] = os.uname()[1]

from sip.common.resource_manager import ResourceManager
from sip.common.docker_paas import DockerPaas as Paas
from sip.master import config
from sip.zmq_logging_aggregator.zmq_logging_handler import ZmqLogHandler
from sip.master.master_states import MasterControllerSM
from sip.master.slave_poller import SlavePoller
from sip.master.rpc_service import RpcService
from sip.master.reconnect import reconnect
from sip.master.shutdown import Shutdown

NAME = "sip.MasterController"


def main():
    """ Main function.
    """
    # Create a logger object.
    log = logging.getLogger(NAME)

    # Create a docker swarm PaaS object
    platform = Paas()

    # Start logging aggregator service.
    log.debug('Starting ZMQ Logging aggregator service')
    exposed_ports = [logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                     logging.config.DEFAULT_LOGGING_CONFIG_PORT,
                     5555]
    command = ['python3', '-m', 'sip.zmq_logging_aggregator']
    config.logserver = platform.run_service(name='zla',
                                            task='skasip/sip',
                                            ports=exposed_ports,
                                            cmd_args=command)
    # config.logserver = platform.run_service(name='zla',
    #                                         task='skasip/zla',
    #                                         ports=exposed_ports)

    # Get a handle to the logging service.
    log.debug('Requesting handle to the logging service.')
    zla_ = platform.find_task('zla')

    # Get the logging port published by the logging container.
    log.debug('Requesting address of the logging service.')
    host, port = zla_.location(port=logging.handlers.DEFAULT_TCP_LOGGING_PORT)
    log.debug('Logging service found at host=%s, port=%s', host, port)

    # Attach a ZMQ logging handler to the logger
    handler = ZmqLogHandler(host=host, port=port)
    handler.setLevel(logging.DEBUG)
    log.addHandler(handler)

    # Define paths for static configuration files.
    sip_root = os.path.join(os.path.dirname(__file__), '..')
    config_file = os.path.join(sip_root, 'etc', 'slave_map.json')
    resources_file = os.path.join(sip_root, 'etc', 'resources.json')

    # log banner to indicate we are starting the master controller functions
    log.info('#' * 50)
    log.info('# Started SIP Master')
    log.info('#' * 50)

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
    log.debug('Trying to reconnect to existing services.')
    reconnect(platform)

    # For testing we can also post events typed on the terminal
    try:
        log.debug('Starting the CLI')
        # readline.parse_and_bind('tab: complete')

        sm = config.master_controller_state_machine
        while True:
            if os.path.exists("docker_swarm"):
                time.sleep(1)
            else:
                # Read from the terminal and process the event
                command = input('** Enter command: ').split()

                # No command received.
                if not command:
                    print('== Allowed commands: online, offline, shutdown, '
                          'cap [name] [task]')
                    continue

                # State command: Prints the current state.
                if command[0] == 'state':
                    log.info('CLI: Current state: {}'.
                             format(sm.current_state()))
                    continue

                # Log command: Tries to spam some log messages.
                if command[0] == 'log':
                    try:
                        host, port = platform.find_task('zla').location(
                            port=logging.handlers.DEFAULT_TCP_LOGGING_PORT)
                        log.debug('Found zla service on host=%s, port=%s',
                                  host, port)
                    except RuntimeError:
                        log.warning('Logging server not found!')
                        continue
                    for handler in log.handlers:
                        print(handler.__class__.__name__)
                        if handler.__class__.__name__ == 'ZmqLogHandler':
                            print(handler._host, handler._port)
                            if handler._port != port:
                                log.removeHandler(handler)
                    for handler in log.handlers:
                        print(handler.__class__.__name__)
                    # TODO(BM) need to check the logger is still alive on
                    # same port!
                    for _ in range(10):
                        log.info('hi there')
                    continue

                # del command: Try to delete a service.
                if command[0] == 'del':
                    try:
                        platform.find_task(command[1]).delete()
                    except RuntimeError:
                        log.warning('Unable to find task "%s" to stop.',
                                    command[1])
                    continue

                # Other commands: posted an events to the state machine.
                log.info('CLI: !!! Posting event ==> {}'.format(command[0]))
                result = sm.post_event(command)

                # Log the result of posting to the state machine.
                if result == 'rejected':
                    log.warning('CLI: Command "%s" not allowed in current '
                                'state', command[0])
                elif result == 'ignored':
                    log.warning('CLI: Command "%s" ignored!', command[0])
                else:
                    # Print what state we are now in.
                    log.info('CLI: Master controller now in state "%s"',
                             sm.current_state())
    except KeyboardInterrupt:
        # pass
        Shutdown().start()


def init_logging(channel=None, propagate=False, add_stream_handler=True,
                 level=logging.NOTSET):
    """Initialise for a specified channel."""
    log = logging.getLogger(channel)
    log.propagate = propagate
    if add_stream_handler:
        formatter = logging.Formatter("= [%(levelname).1s] %(message)-80s "
                                      "(%(name)s)")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        log.addHandler(handler)
    log.setLevel(level)


if __name__ == '__main__':

    # Initialise logging channels
    init_logging()
    init_logging('sip')
    init_logging('docker', level=logging.INFO)
    init_logging('RPC/12345', level=logging.CRITICAL)
    init_logging('urllib3', level=logging.INFO)

    # Start the service.
    main()
