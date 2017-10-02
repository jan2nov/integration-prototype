# coding: utf-8
""" ZMQ Logging handler.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import logging.handlers
import time

import simplejson as json
import zmq


class ZmqLogFormatter(logging.Formatter):
    """ Formats log messages for the ZmqLogHandler.
    """

    def format(self, record):
        """ Returns a JSON string encoding the log record.

        Args:
            record: Python logging LogRecord object.

        Returns:
            string, JSON formatted LogRecord
        """
        return json.dumps(record.raw, sort_keys=True)


class ZmqLogHandler(logging.Handler):
    """Publishes Python LogRecord objects to a ZMQ PUB socket"""

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
        # pylint: disable=no-member
        logging.Handler.__init__(self, level)
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        address = 'tcp://{}:{}'.format(host, port)
        publisher.connect(address)
        time.sleep(0.1)
        self.channel = channel
        self.zmq_publisher = publisher
        self.formatter = ZmqLogFormatter()

    @staticmethod
    def _to_bytes(value):
        """ Convert unicode argument to bytes

        Args:
            s: Unicode string to convert.

        Returns:
            Input string encoded as a utf8 byte array.
        """
        if isinstance(value, bytes):
            return value
        elif isinstance(value, str):
            return value.encode(encoding='utf8')
        else:
            raise TypeError('Expected unicode or bytes, got %r' % value)

    def emit(self, record):
        """ Publish log messages over ZMQ

        Writes a JSONified LogRecord to the ZMQ PUB socket. THe record is
        converted to JSON by the ZmqLogFormatter class.

        Args:
            record: Python logging LogRecord object.
        """
        b_chan = self._to_bytes(self.channel)
        b_level = self._to_bytes(record.levelname)
        b_chan = b':'.join([b_level, b_chan])
        b_msg = self._to_bytes(self.format(record))
        self.zmq_publisher.send_multipart([b_chan, b_msg])
