# coding: utf-8
""" ZeroMQ based Logging aggregator service class.

This class implements a ZMQ SUB socket.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import pickle
import logging
import logging.config
import logging.handlers
import multiprocessing
import sys
import time

import zmq

from .logging_config import load_logging_config


class ZmqLoggingAggregator(multiprocessing.Process):
    """ZeroMQ logging aggregator service class.

    Example
    -------
    This class can be used as follows to spawn a logging aggregator service::

        service = ZmqLoggingAggregator(config_file)
        service.daemon = True
        service.start()
        service.join()

    Notes
    -----
    This could probably also be a thread as will not block the GIL

    """

    def __init__(self, config_file=None):
        """Constructor.

        Notes
        -----
        As this class is a multiprocessing.Process where the run() method
        defines what is run in the process do not run any code in the init
        that also needs to be in the process spawned by calling start() on this
        class.

        Parameters
        ----------
        config_file : str
            Path of logging configuration file (JSON or YAML).
        """
        multiprocessing.Process.__init__(self)
        self.config_file = config_file

    def __del__(self):
        """Destructor.

        Stops the logging configuration server (socket) from listening for new
        config.
        """
        log_ = logging.getLogger(__name__)
        log_.debug('Stopping the logging configuration server')
        logging.config.stopListening()

    @staticmethod
    def _verify_config(config):
        """Logging configuration server method to validate configuration.

        Parameters
        ----------
        config : str
            Python logging configuration string.

        Returns
        -------
        str
            The verified configuration string
        """
        log = logging.getLogger(__name__)
        log.info('CONFIG RECEIVED: ', config)
        return config

    def _bind(self, port=logging.handlers.DEFAULT_TCP_LOGGING_PORT):
        """ Create and bind the subscriber socket to the specified port.

        Args:
            port (int): Subscriber port.
        """
        log = logging.getLogger(__name__)
        # Create the ZMQ context and subscriber socket.
        log.debug('Creating ZMQ Context')
        self.context = zmq.Context()
        log.debug('Creating ZMQ SUB socket')
        self.subscriber = self.context.socket(zmq.SUB)
        log.debug('Binding to ZMQ SUB socket ...')
        try:
            self.subscriber.bind('tcp://*:{}'.format(port))
            self.subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
            log.debug('ZMQ Socket bound to port: %i', port)
        except zmq.ZMQError as error:
            log.fatal('Failed to connect to ZMQ subscriber socket: %s',
                      error.strerror)
            sys.exit(error.errno)

    def _start_config_server(self,
                             port=logging.config.DEFAULT_LOGGING_CONFIG_PORT):
        """Initialise and start logging configuration server."""
        log = logging.getLogger(__name__)
        # Start a logging configuration server.
        # see: http://bit.ly/logging_config_server
        try:
            self.config_server = logging.config.listen(
                port=port, verify=self._verify_config)
            self.config_server.daemon = True
            self.config_server.start()
            log.debug('Started logging configuration server on port %i', port)
        except OSError:
            log.critical('Unable to start logging configuration server on '
                         'port %i', port)


    @staticmethod
    def _logspace(start, stop, count):
        """Generates a logarithmically spaced list of values.

        Generates a list of count logarithmically spaced points between
        decades 10^start and 10^stop.


        Parameters
        ----------
        start : float
            10 ** start is the starting value of the list.
        stop : float
            10 ** stop is the final value of the list.
        count : int
            Number of samples to generate

        Returns
        -------
        list
            list of count samples, equally spaced on a log scale
        """
        return [pow(10, start + y) for y in (x * ((stop - start) / (count - 1))
                                             for x in range(count))]

    def run(self):
        """Logging aggregator event loop.

        Polls for new log messages on the ZMQ sub socket.
        """
        log_ = logging.getLogger(__name__)

        # Load the default logging configuration.
        if self.config_file:
            load_logging_config(self.config_file)
            log_.info('Loaded config file: %s', self.config_file)

        # Create and bind the ZMQ subscriber socket.
        # self._bind()
        port = 5560
        host = 'localhost'

        # Create the ZMQ context and subscriber socket.
        # FIXME(BM): Need to create a list of sub sockets and update this
        # OR use an proxy
        #    see <http://bit.ly/zmq_dynamic_discovery>
        # -------------------------------------------
        log_.debug('Creating ZMQ SUB socket')
        sub = zmq.Context(io_threads=1).socket(zmq.SUB)
        # sub.set_hwm(1)
        log_.debug('Socket HWM = %i', sub.get_hwm())
        log_.debug('Binding to ZMQ SUB socket ...')
        try:
            sub.connect('tcp://{}:{}'.format(host, port))
            sub.setsockopt_string(zmq.SUBSCRIBE, '')
            log_.debug('ZMQ Socket bound to port: %i', port)
        except zmq.ZMQError as error:
            log_.fatal('Failed to connect to ZMQ subscriber socket: %s',
                       error.strerror)
            sys.exit(error.errno)
        # ---------------------------------------------

        # Create and start logging configuration server
        # self._start_config_server()

        # Exponential relaxation of the timeout in the event loop.
        fail_count = 0
        fail_count_limit = 50
        timeout = self._logspace(-4, -1, fail_count_limit)
        message_count = 0
        time_of_first_message = time.time()
        time_of_last_message = time.time()
        zmq_logger = logging.getLogger('sip')

        socket = sub
        # TODO(BM) can this be replaced with a zmq poller?
        # see: https://goo.gl/bKHM2v
        log_.info('Starting SIP ZMQ Logging aggregator event loop')
        while True:
            # Try to receive and display a log message.
            try:
                topic, values = socket.recv_multipart(flags=zmq.NOBLOCK)
                record = pickle.loads(values)
                # Reset the message fail counter.
                fail_count = 0
                if message_count == 0:
                    time_of_first_message = time.time()
                    log_.debug('Log record received, event loop timeout reset!')
                message_count += 1
                time_of_last_message = time.time()
                zmq_logger.handle(record)
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
