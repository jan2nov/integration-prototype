# coding: utf-8
""" Mock logging publisher.

Mock service that publishes logs to over a ZMQ PUB socket.
"""
import logging
import logging.handlers
import sys
from time import sleep, asctime
from os import getpid
from random import choice

from sip.zmq_logging_subscriber import ZmqLogHandler

NAME = sys.argv[1] if len(sys.argv) == 2 else \
    'publisher_pid-{}'.format(getpid())


def write_log(bunch_size=1000, bunch_interval=2, total_bunches=None):
    """Write a series of log messages in bunches

    Parameters
    ----------
    bunch_size : int
        Number of log messages to write per bunch
    bunch_interval : float
        Number of seconds between each bunch
    total_bunches : int or None, optional
        If not None, number of bunches to send before exiting

    """
    local_logger = logging.getLogger()
    logger = logging.getLogger(NAME)
    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG
    ]
    local_logger.info('Bunch size = %i, bunch interval = %f s',
                      bunch_size, bunch_interval)
    if total_bunches is not None:
        local_logger.info('Total bunches = %i', total_bunches)
    bunch_index = 0
    i = 1
    while True:
        logger.log(choice(levels), 'Hello #%04i.%04i @ %s',
                   bunch_index, i, asctime())
        i += 1
        if i % bunch_size == 0:

            bunch_index += 1
            i = 0
            if total_bunches is not None and total_bunches == bunch_index:
                break
            sleep(bunch_interval)


def init_local_logger(level=logging.DEBUG):
    """Initialise a local (stdout) logger."""
    log = logging.getLogger()
    log.propagate = False
    formatter = logging.Formatter('= [%(levelname).1s] %(message)-60s '
                                  '(%(name)s)')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(level)
    return log


def init_zmq_logger(level=logging.NOTSET):
    """Initialise a logger which sends messages over a ZeroMQ PUB socket."""
    log = logging.getLogger(NAME)
    log.propagate = False
    log.setLevel(level)
    handler = ZmqLogHandler()
    handler.setLevel(level)
    log.addHandler(handler)


def main():
    """Mock ZeroMQ Logging publisher main"""
    # Set up a local logging channel going to stdout.
    init_local_logger()

    # Set up a logging object with a ZMQ PUB handler.
    init_zmq_logger(level=logging.NOTSET)

    # Create a local logging object and attach a stream handler.
    local_log = logging.getLogger('local.' + NAME)
    local_log.info('Running mock publisher with name: "%s"', str(NAME))
    local_log.debug('Sending messages ...')
    write_log(bunch_size=100, bunch_interval=0.1)
    local_log.debug('Done.')


if __name__ == '__main__':
    main()
