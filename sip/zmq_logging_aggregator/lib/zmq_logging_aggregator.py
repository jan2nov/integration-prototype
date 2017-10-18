# coding: utf-8
""" ZeroMQ based Logging aggregator service class.

This class implements a ZMQ SUB socket.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import threading
import logging
import logging.handlers
import json
import time

import zmq

from .record_factory import LogRecordFactory
from .logging_config import load_logging_config


class ZmqLoggingAggregator(threading.Thread):
    """ ZeroMQ logging aggregator service."""

    def __init__(self, config_file):
        """ Initialise"""
        threading.Thread.__init__(self)
        log = logging.getLogger(__name__)

        # Define an event used to stop the thread.
        self._stop_requested = threading.Event()

        # Load the default logging configuration.
        log.debug('Loading config file: %s.', config_file)
        load_logging_config(config_file)
        log.debug('Config file loaded.')

        # Create the ZMQ context and subscriber socket.
        log.debug('Creating ZMQ Context')
        self.context = zmq.Context()
        log.debug('Creating ZMQ SUB socket')
        self.subscriber = self.context.socket(zmq.SUB)

        # Set the LogRecord object
        log_factory = LogRecordFactory()
        logging.setLogRecordFactory(log_factory.log)

        # Bind the ZMQ subscriber socket.
        log.debug('Binding to ZMQ SUB socket')
        self._connect()

    def stop(self):
        """ Stop the thread
        """
        self._stop_requested.set()

    def _connect(self, port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        """Bind the subscriber socket to the specified port.

        Args:
            port (int): Subscriber port.
        """
        log = logging.getLogger(__name__)
        try:
            self.subscriber.bind('tcp://*:{}'.format(port))
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
        except zmq.ZMQError as error:
            log.error('Failed to connect to ZMQ subscriber socket: %s',
                      error.msg())
            raise

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
        log = logging.getLogger(__name__)
        log.info('Started SIP ZMQ Logging aggregator')

        # Exponential relaxation of the timeout in the event loop.
        fail_count = 0
        fail_count_limit = 50
        timeout = [10**exp for exp in self._linspace(-4, -1, fail_count_limit)]
        message_count = 0
        time_of_first_message = time.time()
        time_of_last_message = time.time()

        while not self._stop_requested.is_set():

            # Try to receive and display the log message.
            try:
                topic, values = self.subscriber.recv_multipart(zmq.NOBLOCK)
                str_values = values.decode('utf-8')
                try:
                    dict_values = json.loads(str_values)
                    dict_values['args'] = tuple(dict_values['args'])
                    record = logging.makeLogRecord(dict_values)
                    fail_count = 0
                    if message_count == 0:
                        time_of_first_message = time.time()
                        print('Message timer reset!')
                    message_count += 1
                    time_of_last_message = time.time()
                    log.handle(record)
                except json.decoder.JSONDecodeError:
                    log.error('Unable to decode JSON log record.')
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
                print('Reached timeout limit of {:.2f}s, '
                      '({} messages received in {:.2f}s)'
                      .format(_timeout, message_count,
                              (time_of_last_message - time_of_first_message)))
                message_count = 0

            # TODO(BM) have a different log for messages from the aggregator
            # vs those received. (eg. log vs log_local)
            # if fail_count % 5 == 0:
            #     log_local.debug('Polling for log messages (fails = %-5i, '
            #                     'timeout = %.4f s)', fail_count, _timeout)

            self._stop_requested.wait(_timeout)
