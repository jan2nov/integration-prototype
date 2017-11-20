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

from .zmq_logging_aggregator import ZmqLoggingAggregator


def start_healthcheck_endpoint(service_process):
    """Start a healthcheck endpoint.

    Simple Bottle web application serving a REST endpoint
    at the URL /healthcheck on port 5555 using a bjoern WSGI server.

    Parameters
    ----------
    service_process : sip.zmq_logging_aggregator.ZmqLoggingAggregator
        Logging service object to monitor health of.
    """
    logger = logging.getLogger(__name__)

    start_time = time.time()
    app = Bottle()

    @app.route('/healthcheck')
    def health_check():
        """ Health check HTTP endpoint
        """
        elapsed = time.time() - start_time
        return dict(module='zmq_logging_aggregator',
                    running=service_process.is_alive(),
                    hostname=socket.gethostname(),
                    uptime=elapsed)
    try:
        bjoern.run(app, host='0.0.0.0', port=5555)
    except OSError as error:
        logger.critical("ERROR: Unable to start healthcheck API: %s",
                        error.strerror)


def init_logger(channel, format_string, level=logging.DEBUG):
    """Initialise a logger.

    Parameters
    ----------
    channel : str
        The Python logger channel to initialise
    format_string : str
        Python logging format string which with to configure the logger.
    level : int or str, optional
        Python logging level.
    """
    log = logging.getLogger(channel)
    log.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format_string, '%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    log.setLevel(level)
    log.addHandler(handler)


def main():
    """SIP ZMQ Logging aggregator service main."""
    log = logging.getLogger(__name__)

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
    # Define the root logger.
    LOG = logging.getLogger()
    LOG.setLevel(logging.NOTSET)

    # Initialise a logger for aggregated messages.
    FORMAT_STR = "> [%(levelname).1s] %(message)-80s " \
                 "(%(name)s:L%(lineno)i) [%(asctime)s]"
    init_logger(channel='',
                format_string=FORMAT_STR,
                level=logging.DEBUG)

    main()
