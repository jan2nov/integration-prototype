# coding: utf-8
""" Unit tests for the ZMQ logging handler.

Run with:
    $ python3 -m unittest discover -f -v -p test_zmq_logging_handler.py

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import unittest
import unittest.mock
import logging
import time
import requests


from sip.zmq_logging_handler.zmq_logging_handler import ZmqLogHandler


class TestZmqLoggingHandler(unittest.TestCase):
    """ Tests of the ZMQ logging handler.
    """

    def test_connect_fail(self):
        """ Check that an exception is raised the handler cant connect.
        """
        self.assertRaises(requests.exceptions.ConnectionError,
                          ZmqLogHandler, host='invalid')

    # def test_connect(self):
    #     """ Check that an connection can be established.
    #     """
    #     service = MockZmqLoggingAggregator()
    #     service.daemon = True
    #     service.start()
    #     try:
    #         _ = ZmqLogHandler(host='localhost')
    #     except requests.exceptions.ConnectionError:
    #         self.fail('Unexpected exception raised.')
    #     service.stop()
    #     service.join()
    #
    # def test_log_info(self):
    #     """ Check that an info message can be sent.
    #     """
    #     log = logging.getLogger('sip.' + __name__ + '-test_log_info')
    #     try:
    #         log.addHandler(ZmqLogHandler(host='localhost'))
    #         # log.addHandler(logging.StreamHandler())
    #     except requests.exceptions.ConnectionError:
    #         self.fail('Failed to connect handler to subscriber socket.')
    #     log.setLevel(logging.INFO)
    #     time.sleep(0.1)
    #
    #     self.watcher.start()
    #
    #     for i in range(self.send_count):
    #         log.info('hello %03i', i)
    #
    #     while self.watcher.isAlive():
    #         self.watcher.join(timeout=1e-5)

    # def test_log_debug(self):
    #     """ Check that an debug message can be sent.
    #     """
    #
    # def test_log_warning(self):
    #     """ Check that an warning message can be sent.
    #     """


if __name__ == '__main__':
    unittest.main()
