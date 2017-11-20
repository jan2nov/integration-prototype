# coding: utf-8
"""ZeroMQ proxy used for pub-sub logging.

http://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/devices/forwarder.html
"""

from time import sleep
from threading import Thread
import zmq
import zmq.devices


def main():
    """

    https://gist.github.com/minrk/4667957


    Returns
    -------

    """
    try:
        context = zmq.Context(io_threads=1)

        # Socket facing the clients (publishers)
        frontend = context.socket(zmq.SUB)
        frontend.bind('tcp://*:5559')
        frontend.setsockopt_string(zmq.SUBSCRIBE, '')

        # Socket facing services (subscribers)
        backend = context.socket(zmq.PUB)
        backend.bind('tcp://*:5560')

        zmq.devices.device(zmq.FORWARDER, frontend, backend)

    except Exception as e:
        raise
    finally:
        pass
        frontend.close()
        backend.close()
        context.term()


def broker(context):
    """ https://netmq.readthedocs.io/en/latest/xpub-xsub/"""
    xsub = context.socket(zmq.XSUB)  # IN: Publishers connect to this socket
    xsub.bind('tcp://*:5559')

    xpub = context.socket(zmq.XPUB)  # OUT: Subscribers connect to this socket
    xpub.bind('tcp://*:5560')

    poller = zmq.Poller()
    poller.register(xpub, zmq.POLLIN)
    poller.register(xsub, zmq.POLLIN)
    while True:
        events = dict(poller.poll(timeout=1000))
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


if __name__ == '__main__':
    # main()
    CONTEXT = zmq.Context(io_threads=1)
    THREAD = Thread(target=broker, args=(CONTEXT,))
    THREAD.start()
    while True:
        try:
            sleep(1)
        except KeyboardInterrupt:
            break
    CONTEXT.term()
    THREAD.join()

