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

import requests
import zmq


NAME = sys.argv[1] if len(sys.argv) == 2 else 'mock_log_publisher'


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
    for i in range(1000):
        log.info('%04i. Hello @ %s', i, time.asctime())
        # log.debug('Hello again!')
        # time.sleep(0.0001)


def main():
    """ Main
    """
    print(NAME)
    # Attach a stream handler to the log
    log = logging.getLogger(NAME)
    formatter = logging.Formatter('= %(name).40s | %(levelname)-5s '
                                  '| %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    # log.addHandler(handler)
    log.setLevel(logging.DEBUG)

    # Attach a ZeroMQ handler to the log
    try:
        # FIXME(BM) need to get hostname of log aggregator
        # This will be different if this publisher is run from inside the same
        # overlay network as the subscriber or not.
        handler = ZmqHandler(host='localhost')
        # handler = ZmqHandler(host='www.bbc.co.uk')
        log.addHandler(handler)
        write_log()
    except requests.exceptions.ConnectionError:
        log.error('Unable to connect to logging aggregator')
        sys.exit(1)


if __name__ == '__main__':
    main()
