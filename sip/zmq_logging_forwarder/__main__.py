# coding: utf-8
"""ZeroMQ PUB-SUB logging forwarder (proxy).

This module defines a logging forwarder service to be used with SIP ZMQ
logging.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""
from threading import Thread
from time import sleep, time

import zmq
import zmq.devices

import bjoern
from bottle import Bottle


def heathcheck():
    """Start a healthcheck endpoint.

    Simple Bottle web application serving a REST endpoint
    at the URL /healthcheck on port 5555 using a bjoern WSGI server.
    """
    start_time = time()
    app = Bottle()

    @app.route('/healthcheck')
    def health_check():
        """ Health check HTTP endpoint
        """
        return dict(module='zmq_logging_forwarder',
                    uptime=(time() - start_time))
    try:
        bjoern.run(app, host='0.0.0.0', port=5555)
    except OSError as error:
        print("ERROR: Unable to start healthcheck API: %s" % error.strerror)


def forwarder(context, sub_port=5559, pub_port=5560):
    """Function to forward log messages from subscribers to publishers.

    Parameters
    ----------
    context : zmq.Context
        ZMQ Context object
    sub_port : int, optional
        Port which to bind the zmq.XSUB socket to. This is the port to be
        connected to by publishers.
    pub_port : int, optional
        Port which to bind the zmq.XPUB socket to. This is the port to be
        connected to by subscribers.

    """
    # Create and bind XSUB socket. Publishers should connect to this.
    xsub = context.socket(zmq.XSUB)
    xsub.bind('tcp://*:{}'.format(sub_port))

    # Create and bind XPUB socket. Subscribers should connect to this.
    xpub = context.socket(zmq.XPUB)  # OUT: Subscribers connect to this socket
    xsub.bind('tcp://*:{}'.format(pub_port))

    # Create a ZMQ Poller and register the XSUB and XPUB sockets.
    poller = zmq.Poller()
    poller.register(xpub, zmq.POLLIN)
    poller.register(xsub, zmq.POLLIN)

    # Event loop, wait for events on registered zmq sockets and act.
    while True:
        events = dict(poller.poll(timeout=1000))  # timeout is in ms
        # Events from subscribers
        if xpub in events:
            message = xpub.recv_multipart()
            print('[BROKER] subscription event', message)
            xsub.send_multipart(message)
        # Events from publishers
        if xsub in events:
            message = xsub.recv_multipart()
            # print('[BROKER] publishing message!')
            xpub.send_multipart(message)


def main():
    """Main function."""
    context = zmq.Context(io_threads=1)
    forwarder_thread = Thread(target=forwarder, args=(context,))
    health_check_thread = Thread(target=heathcheck)
    forwarder_thread.start()
    health_check_thread.start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
    context.term()
    forwarder_thread.join(timeout=2000)
    health_check_thread.join(timeout=2000)


if __name__ == '__main__':
    main()
