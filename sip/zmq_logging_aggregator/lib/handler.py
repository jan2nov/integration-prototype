# coding: utf-8
""" ZMQ Logging handler.

This handler is expected to be used by other services who wish to send messages
using ZMQ logging.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import logging
import logging.handlers
import time

import requests
import zmq


class ZmqLogHandler(logging.Handler):
    """Publishes Python LogRecord objects to a ZMQ PUB socket"""

    def __init__(self, channel='all', host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 level=logging.NOTSET):
        """
        Constructor. Creates a Python logging handler object which
        sends JSONified LogRecords to a ZMQ pub socket.

        Note if running a service using a Docker Swarm overlay network the
        host will be the container name of the ZMQ logging aggregator.

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
        time.sleep(0.1)  # FIXME(BM) remove this sleep!
        self.channel = channel
        self.zmq_publisher = publisher

    def emit(self, record):
        """ Publish log messages over ZMQ

        Writes a JSONified LogRecord to the ZMQ PUB socket.

        Args:
            record: Python logging LogRecord object.
        """
        b_chan = self._to_bytes(self.channel)
        b_level = self._to_bytes(record.levelname)
        b_chan = b':'.join([b_level, b_chan])
        b_msg = self._to_bytes(json.dumps(record.__dict__.copy()))
        self.zmq_publisher.send_multipart([b_chan, b_msg])

    @staticmethod
    def _to_bytes(unicode):
        """ Convert unicode argument to bytes

        Args:
            unicode: Unicode string to convert.

        Returns:
            Input string encoded as a utf8 byte array.
        """
        if isinstance(unicode, bytes):
            return unicode
        elif isinstance(unicode, str):
            return unicode.encode(encoding='utf8')
        else:
            raise TypeError('Expected unicode or bytes, got %r' % unicode)
