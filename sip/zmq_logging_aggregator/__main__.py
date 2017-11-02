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


if __name__ == '__main__':
    # Define a logging formatter and handler.
    SIP = logging.getLogger('sip')
    SIP_FORMAT = logging.Formatter("> [%(levelname).1s] %(message)-50s "
                                   "(%(name)s:L%(lineno)i)")
    SIP_HANDLER = logging.StreamHandler()
    SIP_HANDLER.setFormatter(SIP_FORMAT)
    SIP.addHandler(SIP_HANDLER)
    SIP.setLevel(logging.DEBUG)

    # Set the default local ZeroMQ Logging aggregator logging handler.
    ZLA = logging.getLogger('zla')
    ZLA.propagate = False
    ZLA_HANDLER = logging.StreamHandler()
    ZLA_FORMAT = logging.Formatter("= [%(levelname).1s] %(message)s")
    ZLA_HANDLER.setFormatter(ZLA_FORMAT)
    ZLA.addHandler(ZLA_HANDLER)
    ZLA.setLevel(logging.DEBUG)

    main()
