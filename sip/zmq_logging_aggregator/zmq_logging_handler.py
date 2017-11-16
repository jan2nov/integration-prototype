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

import zmq


class ZmqLogHandler(logging.Handler):
    """Publishes Python LogRecord objects to a ZMQ PUB socket"""

    def __init__(self, zmq_channel='all', host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 level=logging.NOTSET):
        """
        Constructor. Creates a Python logging handler object which
        sends JSONified LogRecords to a ZMQ pub socket.

        Note if running a service using a Docker Swarm overlay network the
        host will be the container name of the ZMQ logging aggregator.

        Args:
            zmq_channel (string): Logging channel name. ZMQ topic.
            host (string): Hostname (of the subscriber) to publish to.
            port (int, string): Port on to publish messages to.
            level (int, string): Logging level.
        """
        log = logging.getLogger(__name__)
        # # FIXME(BM) Dont try the healthcheck here as publishing messages
        # # should NOT depend on a logging aggregator existing!!!
        #
        # health_check_port = 5555
        # health_check_timeout = 2.0
        # # Check the Logging aggregator exists by querying its health check
        # # endpoint. If this fails an exception will be raised which is captured
        # # in the main
        # # FIXME(BM) this wont work if using docker assigned published ports ...
        # health_check_url = ('http://{}:{}/healthcheck'.
        #                     format(host, health_check_port))
        # log.debug('Health check URL: %s', health_check_url)
        # response = requests.get(health_check_url, timeout=health_check_timeout)
        # health_state = response.json()
        # print(json.dumps(health_state, indent=2))
        # if health_state['module'] != 'zmq_logging_aggregator':
        #     raise RuntimeError('Logging aggregator does not exist')
        logging.Handler.__init__(self, level)
        self._host = host
        self._port = port
        self._zmq_channel = zmq_channel
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)  # pylint: disable=no-member
        address = 'tcp://{}:{}'.format(host, port)
        publisher.connect(address)
        log.debug('Connected to ZMQ PUB socket with address: "%s"',
                  address)
        # Sleep to address the slow joiner problem.
        # see: http://zguide.zeromq.org/page:all#Getting-the-Message-Out
        time.sleep(0.5)
        self.zmq_publisher = publisher

    def emit(self, record):
        """ Publish log messages over ZMQ

        Writes a JSONified LogRecord to the ZMQ PUB socket.

        Args:
            record: Python logging LogRecord object.
        """
        b_chan = self._to_bytes(self._zmq_channel)
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
