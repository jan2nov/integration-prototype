# coding: utf-8
""" ZeroMQ logging aggregator service application

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging
import socket
import sys
from time import time, sleep
import pickle
from threading import Thread

import zmq

import bjoern
from bottle import Bottle

# from .zmq_logging_aggregator import ZmqLoggingAggregator


def subscriber_thread(host='localhost', port=5560):
    """Subscriber function connecting to the logging fowarder

    Parameters
    ----------
    host : str
        Host name or IP address of the logging forwarder
    port : int
        Port of the logging forwarder

    """
    local_logger = logging.getLogger(__name__)
    local_logger.debug('Creating ZMQ SUB socket')
    address = 'tcp://{}:{}'.format(host, port)
    context = zmq.Context(io_threads=1)
    sub = context.socket(zmq.SUB)
    sub.connect(address)
    sub.setsockopt_string(zmq.SUBSCRIBE, '')

    zmq_logger = logging.getLogger('sip')
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    while True:
        events = dict(poller.poll(timeout=1000))
        if sub in events:
            topic, message = sub.recv_multipart()
            record = pickle.loads(message)
            zmq_logger.handle(record)


def subscriber_thread_2(port=5559):
    """Subscriber function binding to the SUB port directly.

    Not using the logging forwarder


    Parameters
    ----------
    host : str
        Host name or IP address of the logging forwarder
    port : int
        Port of the logging forwarder

    """
    local_logger = logging.getLogger(__name__)
    local_logger.debug('Creating ZMQ SUB socket')
    address = 'tcp://{}:{}'.format('*', port)
    context = zmq.Context(io_threads=1)
    sub = context.socket(zmq.SUB)  # or XSUB?
    local_logger.debug('Binding to address: "%s"', address)
    sub.bind(address)
    local_logger.debug('Connected.')
    sub.setsockopt_string(zmq.SUBSCRIBE, '')

    zmq_logger = logging.getLogger('sip')
    poller = zmq.Poller()
    poller.register(sub, zmq.POLLIN)
    message_count = 0
    report_interval = 1000
    start_time = time()
    while True:
        events = dict(poller.poll(timeout=1000))
        if sub in events:
            topic, message = sub.recv_multipart()
            record = pickle.loads(message)
            zmq_logger.handle(record)
            message_count += 1
            if message_count % report_interval == 0:
                local_logger.info('Message count = %i '
                                  '(rate = %.2f messages/s)',
                                  message_count,
                                  report_interval / (time() - start_time))
                start_time = time()



def start_healthcheck(service_process):
    """Start a healthcheck endpoint.

    Simple Bottle web application serving a REST endpoint
    at the URL /healthcheck on port 5555 using a bjoern WSGI server.

    Parameters
    ----------
    service_process : sip.zmq_logging_aggregator.ZmqLoggingAggregator
        Logging service object to monitor health of.
    """
    logger = logging.getLogger(__name__)

    start_time = time()
    app = Bottle()

    @app.route('/healthcheck')
    def health_check():
        """ Health check HTTP endpoint
        """
        return dict(module='zmq_logging_subscriber',
                    running=service_process.is_alive(),
                    hostname=socket.gethostname(),
                    uptime=time() - start_time)
    try:
        bjoern.run(app, host='0.0.0.0', port=5555)
    except OSError as error:
        logger.critical("ERROR: Unable to start healthcheck API: %s",
                        error.strerror)


def init_logger(channel, format_string, level=logging.DEBUG):
    """Initialise a logger.

    Parameters
    ----------
    channel : str
        The Python logger channel to initialise
    format_string : str
        Python logging format string which with to configure the logger.
    level : int or str, optional
        Python logging level.
    """
    log = logging.getLogger(channel)
    log.propagate = False
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format_string, '%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(level)
    log.setLevel(level)
    log.addHandler(handler)


def main():
    """SIP ZMQ Logging aggregator service main."""
    log = logging.getLogger(__name__)

    try:
        # Start the ZMQ logging aggregator.
        config_file = None
        if len(sys.argv) > 1:
            config_file = sys.argv[1]
        # service = ZmqLoggingAggregator(config_file)
        # service.daemon = True
        # service.start()
        # healthcheck_endpoint(service)
        # service.join()
        # sub_host = 'localhost'
        # sub_port = 5560
        # sub = Thread(target=subscriber_thread, args=(sub_host, sub_port,))
        pub_port = 5559
        sub = Thread(target=subscriber_thread_2, args=(pub_port,))
        sub.start()

        start_healthcheck(sub)

        sub.join()

    except KeyboardInterrupt:
        # service.terminate()
        log.info('Terminated logging aggregator service')
        sleep(1.0)


if __name__ == '__main__':
    # Define the root logger.
    LOG = logging.getLogger()
    LOG.setLevel(logging.NOTSET)

    # Initialise a logger for aggregated messages.
    FORMAT_STR = "> [%(levelname).1s] %(message)-80s " \
                 "(%(name)s:L%(lineno)i) [%(asctime)s]"
    init_logger(channel='',
                format_string=FORMAT_STR,
                level=logging.DEBUG)

    main()
