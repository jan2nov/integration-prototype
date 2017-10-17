# coding: utf-8
""" Example Logging publisher.

Spams log messages with a ZMQ handler.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import logging.handlers
import time
# import simplejson as json
import json

import zmq


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
        # TODO(BM) check if we can connect to the aggregator by querying the
        # health-check endpoint.
        #   $ curl http://[host]:[port]/health
        logging.Handler.__init__(self, level)
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
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
            raise TypeError('Expected unicode or bytes, got %r' % value)


def main():
    """ Main
    """
    log = logging.getLogger('mock_log_publisher.py')
    for i in range(10):
        log.info('HELLO %i', i)
        log.debug('HELLO AGAIN %i', i)
        time.sleep(0.1)


if __name__ == '__main__':
    # Attach a stream handler to the log
    LOG = logging.getLogger()
    FORMAT = logging.Formatter("= %(name).40s | %(levelname)s | %(message)s")
    HANDLER = logging.StreamHandler()
    HANDLER.setFormatter(FORMAT)
    LOG.addHandler(HANDLER)
    LOG.setLevel(logging.DEBUG)

    # need to get hostname of log aggregator
    # -- This will be different if this publisher is run from inside the same
    #    overlay network as the subscriber or not.
    LOG.addHandler(ZmqHandler())
    main()
