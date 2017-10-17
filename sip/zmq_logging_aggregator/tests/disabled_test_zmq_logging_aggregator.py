# coding: utf-8
""" Unit tests of the ZMQ logging aggregator module.

Run with:
    $ python3 -m unittest discover -f -v -p test_zmq_logging_aggregator.py

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import unittest
import os

from sip.zmq_logging_aggregator.lib.zmq_logging_aggregator import \
    ZmqLoggingAggregator


class TestZmqLoggingAggregator(unittest.TestCase):
    """ Tests of the ZMQ logging aggregator.
    """

    def test_a(self):
        """ ."""
        zla = ZmqLoggingAggregator(os.path.join(
            'sip', 'zmq_logging_aggregator', 'config', 'default.json'))
        # zla.start()

    def test_logging(self):
        """ Test normal logging.

        Starts the logging aggregator thread
        Starts a mock log publisher in another thread

        Checks that the stdout in the log aggregator is as expected.
        """
        pass


