# coding: utf-8
""" ZMQ Logging handler.

This handler is expected to be used by other services who wish to send messages
using ZMQ logging.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import logging.handlers
import pickle

import zmq


class ZmqLogHandler(logging.Handler):
    """Publishes Python LogRecord objects to a ZMQ PUB socket"""

    def __init__(self, zmq_channel='all', host='localhost',
                 port=5559, level=logging.NOTSET):
        """Constructor.

        Creates a Python logging handler object which
        sends JSONified LogRecords to a ZMQ pub socket.

        Note if running a service using a Docker Swarm overlay network the
        host will be the container name of the ZMQ logging aggregator.

        Args:
            zmq_channel (string): Logging channel name. ZMQ topic.
            host (string): Hostname zmq proxy / forwarder to connect to.
            port (int, string): Port on to publish messages to.
            level (int, string): Logging level.
        """
        log = logging.getLogger(__name__)
        logging.Handler.__init__(self, level)
        self._port = port
        self._zmq_channel = zmq_channel

        context = zmq.Context(io_threads=1)
        publisher = context.socket(zmq.PUB)  # pylint: disable=no-member
        # Socket high water mark.
        # ~number of messages that can be pushed to the socket before
        # messages are dropped. see: http://bit.ly/zmq_hwm
        publisher.set_hwm(1000)  # This sets the message buffer size (default:
        address = 'tcp://{}:{}'.format(host, port)
        log.debug('Connecting ZMQ PUB socket to: "%s"', address)
        publisher.connect(address)
        log.debug('Connected.')
        self.zmq_publisher = publisher

    def emit(self, record):
        """Emit a log message on the pub socket belonging to this class.

        Writes a serialised LogRecord to the ZMQ PUB socket.

        Parameters
        ----------
        record: logging.LogRecord
            Python logging LogRecord object.
        """
        b_chan = self._to_bytes(self._zmq_channel)
        b_level = self._to_bytes(record.levelname)
        b_chan = b':'.join([b_level, b_chan])
        b_msg = pickle.dumps(record, protocol=4)
        self.zmq_publisher.send_multipart([b_chan, b_msg])

    @staticmethod
    def _to_bytes(unicode):
        """ Convert unicode argument to bytes

        Args:
            unicode: Unicode string to convert.

        Returns:
            Input string encoded as a utf8 byte array.
        """
        # FIXME(BM) is this method really needed?
        # Channel and levelname can be converted to bytes by other method?
        if isinstance(unicode, bytes):
            return unicode
        elif isinstance(unicode, str):
            return unicode.encode(encoding='utf8')
        else:
            raise TypeError('Expected unicode or bytes, got %r' % unicode)
