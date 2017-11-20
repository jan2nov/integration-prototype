# coding: utf-8
"""Python logging publisher using the native ZMQ logging handler.


Unfortunately this does not send logging metadata otherwise it could be used
in place of the custom sip zmq handler.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import logging
import logging.handlers
from random import choice
from time import sleep
from multiprocessing import Process

import zmq
from zmq.log.handlers import PUBHandler


def publisher():
    """ZMQ logging publisher main function."""

    # Create a ZMQ logging publisher
    pub = zmq.Context().socket(zmq.PUB)
    pub.bind('tcp://*:{}'.format(logging.handlers.DEFAULT_TCP_LOGGING_PORT))
    handler = PUBHandler(pub)
    handler.root_topic = 'my_program'

    logger = logging.getLogger()
    logger.addHandler(handler)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('[%(levelname)-8s] %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    levels = [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG
    ]
    print(levels)

    try:
        i = 0
        while True:
            logger.log(choice(levels), 'hello {}'.format(i))
            sleep(0.5)
            i += 1
    except KeyboardInterrupt:
        print('Ctrl-C caught: Exiting publisher.')


def subscriber():
    """ZMQ logging subscriber main function."""
    print('starting subscriber...')
    sub = zmq.Context().socket(zmq.SUB)
    sub.connect('tcp://localhost:{}'
                .format(logging.handlers.DEFAULT_TCP_LOGGING_PORT))
    topic = ''
    sub.setsockopt_string(zmq.SUBSCRIBE, topic)
    print('waiting for message ...')
    message = sub.recv_multipart()
    print('here')
    print(message)


def main():
    """Main function."""
    pub = Process(target=publisher)
    sub = Process(target=subscriber)
    try:
        pub.start()
        sub.start()
        pub.join()
        sub.join()
    except KeyboardInterrupt:
        print('Terminating publisher.')
        pub.terminate()
        print('Terminating subscriber.')
        sub.terminate()


if __name__ == '__main__':
    main()
