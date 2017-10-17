# coding: utf-8
"""Script that takes a filename and sends it to the server, properly preceded
with the binary-encoded length, as the new logging configuration.

.. moduleauthor:: Benjamin Mort <benjamin.mort@oerc.ox.ac.uk>
"""

import socket
import struct
import sys


def main():
    """Sends a JSON logging configuration file to the SIP
    logging aggregator service."""
    with open(sys.argv[1], 'rb') as file:
        data_to_send = file.read()
    host = 'localhost'
    port = 9999

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(True)
    try:
        sock.connect((host, port))
    except socket.timeout:
        print('Socket failed to connect ...')
    print('Socket connected to address:', sock.getpeername())
    sock.sendall(struct.pack('>L', len(data_to_send)))
    sock.sendall(data_to_send)
    sock.close()


if __name__ == '__main__':
    main()
