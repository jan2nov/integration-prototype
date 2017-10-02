# coding=utf-8
""" LogRecord factory method

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import datetime
import getpass
import logging
import socket


class LogRecordFactory:
    """ Class for creating custom LogRecord objects

    Intended to be used to extend Python logging and used with the
    logging.setLogRecordFactory() method which was added in Python 3.2
    """
    # pylint: disable=too-few-public-methods,no-self-use
    def __init__(self):
        """ Save a copy of te default LogRecord factory
        """
        self.default_log_record_factory = logging.getLogRecordFactory()

    def log(self, *args, **kwargs):
        """ Create LogRecord objects
        """
        # record = logging.getLogRecordFactory()(*args, **kwargs)
        record = self.default_log_record_factory(*args, **kwargs)

        record.hostname = socket.gethostname()
        record.username = getpass.getuser()
        record.origin = '{}.{}:{}'.format(record.module, record.funcName,
                                          record.lineno)
        record.time = datetime.datetime.utcnow().isoformat()
        record.json = record.__dict__.copy()
        return record
