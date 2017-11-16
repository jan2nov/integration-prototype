# coding: utf-8
""" ZeroMQ logging aggregator service application

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import socket
import sys
import time

import bjoern
from bottle import Bottle

from .lib.zmq_logging_aggregator import ZmqLoggingAggregator


def start_healthcheck_endpoint(service):
    """ Start the healthcheck endpoint.

    This is simple Bottle web application serving a REST endpoint
    at the URL /healthcheck on port 5555 using a bjoern WSGI server.
    """
    start_time = time.time()
    app = Bottle()

    @app.route('/healthcheck')
    def health_check():
        """ Health check HTTP endpoint
        """
        elapsed = time.time() - start_time
        return dict(module='zmq_logging_aggregator',
                    running=service.is_alive(),
                    hostname=socket.gethostname(),
                    uptime=elapsed)

    bjoern.run(app, host='0.0.0.0', port=5555)


def main():
    """ SIP ZMQ Logging aggregator service main.
    """
    log = logging.getLogger('zla')

    try:
        # Start the ZMQ logging aggregator.
        config_file = None
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        service = ZmqLoggingAggregator(config_file)
        service.daemon = True
        service.start()
        start_healthcheck_endpoint(service)
        service.join()

    except KeyboardInterrupt:
        service.terminate()
        log.info('Terminated logging aggregator service')


def init_logger(name, format_string, level=logging.DEBUG):
    """Initialise a logger.
    """
    log = logging.getLogger(name)
    log.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format_string, '%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    log.setLevel(level)
    log.addHandler(handler)


if __name__ == '__main__':
    # Define the root logger.
    LOG = logging.getLogger()
    LOG.setLevel(logging.NOTSET)

    # Initialise a logger for local messages.
    init_logger(name='zla',
                format_string="= [%(levelname).1s] %(message)s",
                level=logging.DEBUG)

    # Initialise a logger for aggregated messages.
    FORMAT_STR = "> [%(levelname).1s] %(message)-80s " \
                 "(%(name)s:L%(lineno)i) [%(asctime)s]"
    init_logger(name='sip',
                format_string=FORMAT_STR,
                level=logging.DEBUG)

    main()
