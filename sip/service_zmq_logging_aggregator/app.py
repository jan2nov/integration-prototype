# coding: utf-8
""" Logging aggregator service application

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import signal
import logging
import sys
import os
import time
import socket

from flask import Flask

from .lib.zmq_logging_aggregator import ZmqLoggingAggregator

APP = Flask(__name__)
START_TIME = time.time()


def signal_handler(signum, frame):
    """ Signal handler.

    Args:
        signum: Signal number received.
        frame: The current stack frame
    """
    # pylint: disable=unused-argument
    log = logging.getLogger(__name__)
    print(__name__)
    log.info('ZMQ Logging aggregator service received SIGINT')
    sys.exit(0)


@APP.route('/health')
def health_check():
    """ Health check HTTP endpoint
    """
    elapsed = time.time() - START_TIME
    return ('The SIP ZMQ Logging aggregator (zla) has been running on '
            'hostname {} for {:.1f} s' .format(socket.gethostname(), elapsed))


def main():
    """ SIP ZMQ Logging aggregator service main.
    """
    log = logging.getLogger(__name__)
    signal.signal(signal.SIGINT, signal_handler)

    # Get path of config file.
    # TODO(BM) allow config to be set on command line?
    config_file = os.path.join(os.path.dirname(__file__),
                               'config', 'default.json')
    log.debug('Config file = %s', config_file)

    # Start a logging configuration server.
    config_server = logging.config.listen(port=9999)
    config_server.daemon = True
    config_server.start()

    # Start logging aggregator thread.
    log.debug('Starting ZMQ logging aggregator')
    aggregator = ZmqLoggingAggregator(config_file)
    aggregator.daemon = True
    aggregator.start()

    # Start the HTTP health check endpoint using the Flask development server.
    # FIXME(BM) this is not the correct way to deploy a web service endpoint
    APP.run(host='0.0.0.0', port=5555)

    # Wait until the logging aggregator thread terminates.
    log.debug('Terminating logging aggregator service.')
    aggregator.join()

    log.debug('Terminating logging configuration server.')
    logging.config.stopListening()
    config_server.join()
