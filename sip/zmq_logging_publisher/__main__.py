# coding: utf-8
""" Mock logging publisher.

Mock service that publishes logs to over a ZMQ PUB socket.
"""
import logging
import sys
import time
from random import randint

import requests

from sip.zmq_logging_handler.zmq_logging_handler import ZmqLogHandler

NAME = sys.argv[1] if len(sys.argv) == 2 else \
    'mock_log_publisher-{:04d}'.format(randint(0, 9999))


def write_log():
    """ Write a series of log messages.
    """
    log = logging.getLogger(NAME)
    for i in range(10000):
        log.info('Hello #%04i @ %s', i, time.asctime())
        log.debug('Hello again!')
        time.sleep(0.0001)


def main():
    """ Mock ZeroMQ Logging publisher main
    """
    # Create a local logging object and attach a stream handler.
    local_log = logging.getLogger('local.' + NAME)
    local_log.info('Running mock publisher with name: "%s"', str(NAME))
    local_log.debug('Sending messages ...')
    write_log()
    local_log.debug('Done.')


def init_local_logger(level=logging.DEBUG):
    """ Initialise a local (stdout) logger.
    """
    log = logging.getLogger('local.' + NAME)
    formatter = logging.Formatter('= [%(levelname).1s] %(message)s (%(name)s)')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(level)
    return log


def init_zmq_logger(hostname='zla', level=logging.DEBUG):
    """ Initialise a logger which sends messages over a ZeroMQ PUB socket.
    """
    log = logging.getLogger(NAME)
    log.setLevel(level)
    log.addHandler(ZmqLogHandler(host=hostname))


if __name__ == '__main__':

    # Set up a local logging channel going to stdout.
    init_local_logger()

    # Set up a logging object with a ZMQ PUB handler.
    init_zmq_logger(hostname='zla', level=logging.INFO)

    # Run the main function.
    main()

