# coding: utf-8
""" Unit tests for the ZMQ logging handler.

Run with:
    $ python3 -m unittest discover -f -v -p test_zmq_logging_handler.py

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import unittest
import requests

from sip.zmq_logging_handler.zmq_logging_handler import ZmqLogHandler


class TestZmqLoggingHandler(unittest.TestCase):
    """ Tests of the ZMQ logging handler.
    """

    def test_connect_fail(self):
        """ Check that an exception is raised the handler cant connect.
        """
        self.assertRaises(requests.exceptions.ConnectionError,
                          ZmqLogHandler, host='foo')

    def test_connect(self):
        """ Check that an connection can be established.
        """

    def test_log_info(self):
        """ Check that an info message can be sent.
        """

    def test_log_debug(self):
        """ Check that an debug message can be sent.
        """

    def test_log_warning(self):
        """ Check that an warning message can be sent.
        """
