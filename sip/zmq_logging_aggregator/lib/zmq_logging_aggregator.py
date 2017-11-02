# coding: utf-8
""" ZeroMQ based Logging aggregator service class.

This class implements a ZMQ SUB socket.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import logging
import logging.config
import logging.handlers
import threading
import sys
import time

import zmq

from .logging_config import load_logging_config


# FIXME(BM) convert to multiprocessing.Process
# While this just needs 2 lines of code change if using Process for some
# Reason the ZMQ socket blocks on the receive.
# This needs review see: https://goo.gl/P68YEo


class ZmqLoggingAggregator(threading.Thread):
    """ ZeroMQ logging aggregator service."""

    def __init__(self, config_file=None):
        """ Initialise
        """
        threading.Thread.__init__(self)

        log_ = logging.getLogger('zla')

        # Load the default logging configuration.
        if config_file:
            load_logging_config(config_file)
            log_.debug('Loaded config file: %s', config_file)

        # Create the ZMQ context and subscriber socket.
        log_.debug('Creating ZMQ Context')
        self.context = zmq.Context()
        log_.debug('Creating ZMQ SUB socket')
        self.subscriber = self.context.socket(zmq.SUB)

        # Bind the ZMQ subscriber socket.
        log_.debug('Binding to ZMQ SUB socket')
        self._connect()

        # Start a logging configuration server.
        # https://docs.python.org/3.6/library/logging.config.html#logging.config.listen
        port = logging.config.DEFAULT_LOGGING_CONFIG_PORT
        self.config_server = logging.config.listen(port=port,
                                                   verify=self._verify_config)
        self.config_server.daemon = True
        self.config_server.start()

        log_.debug('ZMQ Logging aggregator initialisation complete.')

    def __del__(self):
        """ Destructor"""
        log_ = logging.getLogger('zla')
        log_.debug('Stopping logging configuration server')
        # logging.config.stopListening()
        # self.config_server.join(timeout=1.0)

    @staticmethod
    def _verify_config(config):
        """ Function to verity that the Logging Config sent to the logging
            configuration server is valid.
        """
        log = logging.getLogger('zla')
        log.info('CONFIG RECEIVED: ', config)
        return config

    def _connect(self, port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        """Bind the subscriber socket to the specified port.

        Args:
            port (int): Subscriber port.
        """
        log_ = logging.getLogger('zla')
        try:
            self.subscriber.bind('tcp://*:{}'.format(port))
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
            log_.debug('ZMQ Socket bound to port: %i', port)
        except zmq.ZMQError as error:
            log_.fatal('Failed to connect to ZMQ subscriber socket: %s',
                       error.strerror)
            sys.exit(error.errno)

    @staticmethod
    def _linspace(start, stop, number):
        """ Generates number values between start and stop.
        """
        if number == 1:
            yield stop
            return
        inc = (stop - start) / (number - 1)
        for i in range(number):
            yield start + inc * i

    def run(self):
        """ Logging aggregator event loop.

        Polls for new log messages on the ZMQ sub socket.
        """
        log_ = logging.getLogger('zla')

        # Exponential relaxation of the timeout in the event loop.
        fail_count = 0
        fail_count_limit = 50
        timeout = [10**exp for exp in self._linspace(-4, -1, fail_count_limit)]
        message_count = 0
        time_of_first_message = time.time()
        time_of_last_message = time.time()
        log = logging.getLogger('sip')
        socket = self.subscriber

        log_.info('Starting SIP ZMQ Logging aggregator event loop')
        while True:
            # Try to receive and display a log message.
            try:
                topic, values = socket.recv_multipart(flags=zmq.NOBLOCK)
                str_values = values.decode('utf-8')
                try:
                    dict_values = json.loads(str_values)
                    dict_values['args'] = tuple(dict_values['args'])
                    record = logging.makeLogRecord(dict_values)
                    fail_count = 0
                    if message_count == 0:
                        time_of_first_message = time.time()
                        log_.debug('Message timer reset!')
                    message_count += 1
                    time_of_last_message = time.time()
                    log.handle(record)
                except json.decoder.JSONDecodeError:
                    log_.error('Unable to decode JSON log record.')
                    raise
            except zmq.ZMQError as error:
                if error.errno == zmq.EAGAIN:
                    fail_count += 1
                else:
                    raise  # Re-raise the exception

            # Set the timeout.
            if fail_count < fail_count_limit:
                _timeout = timeout[fail_count]
            else:
                _timeout = timeout[-1]

            if fail_count == fail_count_limit:
                log_.debug('Reached polling limit of {:.2f}s, '
                           '({} messages received in {:.2f}s)'
                           .format(_timeout, message_count,
                                   (time_of_last_message -
                                    time_of_first_message)))
                message_count = 0
            time.sleep(_timeout)
