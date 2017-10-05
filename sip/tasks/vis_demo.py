#!/usr/bin/python3


""" Skeleton process to be started by slave

"""
import os
import socket
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sip.common.logging_api import log


def _sig_handler(signum, frame):
    sys.exit(0)


def run():

    log.info("INSIDE VIS DEMO")
    # Write to the host file system
    f = open('/mnt/tmp/hello_test', 'w')
    f.close()

    # Read port number
    port = int(sys.argv[1])

    # Bind to socket
    s = socket.socket()
    s.bind(('', port))
    s.listen(1)

    conn, addr = s.accept()
    while (True):
        data = conn.recv(1024)
    conn.close()


if __name__ == '__main__':
    run()
