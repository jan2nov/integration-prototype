# coding: utf-8
""" Example Logging publisher.

Spams log messages with a ZMQ handler.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import logging
import logging.handlers
import sys
import time
from random import randint

import requests
import zmq


NAME = sys.argv[1] if len(sys.argv) == 2 else \
    'mock_log_publisher-{:04d}'.format(randint(0, 9999))


class ZmqHandler(logging.Handler):
    """ Logging handler to which writes messages to a ZMQ PUB socket.
    """

    def __init__(self, channel='all', host='127.0.0.1',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 level=logging.NOTSET):
        """
        Constructor. Creates a Python logging handler object which
        sends JSONified LogRecords to a ZMQ pub socket.

        Args:
            channel (string): Logging channel name. ZMQ topic.
            host (string): Hostname (of the subscriber) to publish to.
            port (int, string): Port on to publish messages to.
            level (int, string): Logging level.
        """
        # Check the Logging aggregator exists by querying its health check
        # endpoint. If this fails an exception will be raised which is captured
        # in the main
        health_check_url = 'http://{}:{}/healthcheck'.format(host, 5555)
        response = requests.get(health_check_url, timeout=2.0)
        health_state = response.json()
        if health_state['module'] != 'zmq_logging_aggregator':
            raise RuntimeError('Logging aggregator does not exist')

        logging.Handler.__init__(self, level)
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)  # pylint: disable=no-member
        address = 'tcp://{}:{}'.format(host, port)
        publisher.connect(address)
        time.sleep(0.1)
        self.channel = channel
        self.zmq_publisher = publisher

    def emit(self, record):
        """ Write a logging record.
        """
        b_chan = self._to_bytes(self.channel)
        b_level = self._to_bytes(record.levelname)
        b_chan = b':'.join([b_level, b_chan])
        b_msg = self._to_bytes(json.dumps(record.__dict__.copy()))
        self.zmq_publisher.send_multipart([b_chan, b_msg])

    @staticmethod
    def _to_bytes(string):
        """ Convert a unicode string to a utf8 byte array, if needed.
        """
        if isinstance(string, bytes):
            return string
        elif isinstance(string, str):
            return string.encode(encoding='utf8')
        else:
            raise TypeError('Expected unicode or bytes, got %r' % string)


def write_log():
    """ Write a series of log messages.
    """
    log = logging.getLogger(NAME)
    for i in range(10):
        log.info('%04i. Hello @ %s', i, time.asctime())
        log.debug('Hello again!')


def main():
    """ Main
    """
    # Create a local logging object and attach a stream handler.
    local_log = logging.getLogger('local.' + NAME)
    formatter = logging.Formatter('= [%(levelname).1s] %(message)s (%(name)s)')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    local_log.addHandler(handler)
    local_log.setLevel(logging.DEBUG)

    # Create a 2nd logging object and attach a ZeroMQ handler.
    log = logging.getLogger(NAME)
    log.setLevel(logging.INFO)
    hosts = ['localhost', 'zla']
    for host in hosts:
        local_log.info('Trying to connect to log aggregator on host %s', host)
        try:
            handler = ZmqHandler(host=host)
            local_log.debug('Connected to log aggregator on host %s', host)
            log.addHandler(handler)
            write_log()
            break
        except requests.exceptions.ConnectionError:
            local_log.warning('Unable to connect to logging aggregator on '
                              'host %s', host)
            if host == hosts[-1]:
                sys.exit(1)
    local_log.info('Running mock publisher with name: %s', str(NAME))


if __name__ == '__main__':
    main()
