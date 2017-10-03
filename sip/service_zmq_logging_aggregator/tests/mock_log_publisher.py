# coding: utf-8
""" Example Logging publisher.

Spams log messages with a ZMQ handler.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import time
import simplejson as json

import zmq


class ZmqFormatter(logging.Formatter):
    """ Formats log messages."""

    def format(self, record):
        """ Returns a formatted log message
        """
        return json.dumps(record.json, sort_keys=True)


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
        logging.Handler.__init__(self, level)
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        address = 'tcp://{}:{}'.format(host, port)
        publisher.connect(address)
        time.sleep(0.1)
        self.channel = channel
        self.zmq_publisher = publisher
        self.formatter = ZmqFormatter()

    def emit(self, record):
        """ Write a logging record.
        """
        log_channel = self._to_bytes(self.channel)
        log_level = self._to_bytes(record.levelname)
        log_channel = b':'.join(log_level, log_channel)
        log_message = self._to_bytes(self.format(record))
        self.zmq_publisher.send_multipart([log_channel, log_message])

    @staticmethod
    def _to_bytes(string):
        """ Convert a unicode string to a utf8 byte array, if needed.
        """
        if isinstance(string, bytes):
            return string
        elif isinstance(string, str):
            return string.encode(encoding='utf8')
        else:
            raise TypeError('Expected unicode or bytes, got %r' % value)


def main():
    """ Main
    """
    log = logging.getLogger(__name__)
    log.info('HELLO')


if __name__ == '__main__':
    # Attach a stream handler to the log
    LOG = logging.getLogger()
    LOG.addHandler(logging.StreamHandler())
    LOG.setLevel(logging.DEBUG)

    # need to get hostname of log aggregator
    # -- This will be different if this publisher is run from inside the same
    #    overlay network as the subscriber or not.
    # LOG.addHandler(ZmqLogHandler())
    main()
