""" Functions executed when the master controller is configured
"""
__author__ = 'David Terrett'

from docker import Client
import os
from pyroute2 import IPRoute
import rpyc
import socket
import threading 
from plumbum import SshMachine
import logging

from sip_common import logger

from sip_master import config
from sip_master import task

class Configure(threading.Thread):
    """ Does the actual work of configuring the system
    """
    def __init__(self):
        super(Configure, self).__init__()

    def run(self):
        """ Thread run routine
        """
        logger.trace('starting configuration')
        
        # Start the local telescope state application
        _start_slave('LTS', config.slave_config['LTS'], 
                config.slave_status['LTS'])

        _start_slave('QA', config.slave_config['QA'], 
                config.slave_status['QA'])

def _find_route_to_logger(host):
    """ Figures out what the IP address of the logger is on 'host'
    """
    addr = socket.gethostbyname(host)
    ip = IPRoute()
    r = ip.get_routes(dst=addr, family=socket.AF_INET)
    for x in r[0]['attrs']:
        if x[0] == 'RTA_PREFSRC':
            return x[1]


def _start_slave(name, cfg, status):
    """ Start a slave controller
    """

    # Start a container if it isn't already running
    if status['state'] == '':
        if cfg['type'] == 'docker':
            _start_docker_slave(name, cfg, status)
        elif cfg['type'] == 'ssh':
            _start_ssh_slave(name, cfg, status)
        else:
            raise RuntimeError('failed to start "' + name + '": "' + cfg['type'] +
                    '" is not a known slave type')

        # Initialise the task status
        status['state'] = 'starting'
        status['new_state'] = 'starting'
        status['timeout counter'] = cfg['timeout']

        # Connect the heartbeat listener to the address it is sending heartbeats
        # to.
        config.heartbeat_listener.connect(status['address'], 
                status['heartbeat_port'])
    else:
        task.load(name, cfg, status)

def _start_docker_slave(name, cfg, status):
    """ Start a slave controller that is a Docker container

        NB This only works on localhost
    """
    # Improve logging soon!
    logging.getLogger('requests').setLevel(logging.DEBUG)

    # Create a Docker client
    client = Client(version='1.21', base_url=cfg['engine_url'])

    # Create a container and store its id in the properties array
    host = config.resource.allocate_host(name, 
            {'launch_protocol': 'docker'}, {})
    image = cfg['image']
    heartbeat_port = config.resource.allocate_resource(name, "tcp_port")
    rpc_port = config.resource.allocate_resource(name, "tcp_port")
    task_control_module = cfg['task_control_module']
    container_id = client.create_container(image=image, 
                   command=['/home/sdp/integration-prototype/slave/bin/slave', 
                            name, 
                            str(heartbeat_port),
                            str(rpc_port),
                            '172.17.0.1',
                            task_control_module,
                           ],
		   volumes=['/home/sdp/tasks/'],
		   host_config=client.create_host_config(binds={
        		os.getcwd()+'/tasks': {
            		'bind': '/home/sdp/tasks/',
            		'mode': 'rw',
        		}
                   }))['Id']

    # Start it
    client.start(container_id)

    info = client.inspect_container(container_id)
    ip_address = info['NetworkSettings']['IPAddress']
    status['address'] = ip_address
    status['container_id'] = container_id
    status['rpc_port'] = rpc_port
    status['heartbeat_port'] = heartbeat_port
    logger.info(name + ' started in container ' + container_id + ' at ' +
                ip_address)

def _start_ssh_slave(name, cfg, status):
    """ Start a slave controller that is a SSH client
    """
    # Improve logging setup!!!
    logging.getLogger('plumbum').setLevel(logging.DEBUG)
   
    # Find a host tht supports ssh
    host = config.resource.allocate_host(name, {'launch_protocol': 'ssh'}, {})

    # Get the root of the SIP installation on that host
    sip_root = config.resource.sip_root(host)

    # Allocate ports for heatbeat and the RPC interface
    heartbeat_port = config.resource.allocate_resource(name, "tcp_port")
    rpc_port = config.resource.allocate_resource(name, "tcp_port")

    # Get the task control module to use for this task
    task_control_module = cfg['task_control_module']

    # Get the address of the logger (as seen from the remote host)
    logger_address = _find_route_to_logger(host)
    print(logger_address)

    ssh_host = SshMachine(host)
    import pdb
    #   pdb.set_trace()
    try:
        py3 = ssh_host['python3']
    except:
        logger.fatal('python3 not available on machine ' + ssh_host)
    logger.info('python3 is available at ' + py3.executable)

    # Construct the command line to start the slave
    cmd = py3[os.path.join(sip_root, 'slave/bin/slave')] \
          [name][heartbeat_port][rpc_port][logger_address][task_control_module]
    ssh_host.daemonic_popen(cmd, stdout= name + '_sip.output')

    status['address'] = host
    status['rpc_port'] = rpc_port
    status['heartbeat_port'] = heartbeat_port
    logger.info(name + ' started on ' + host)
