# coding=utf-8
""" Logging formatter class which truncates the name field.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging


class NameTruncatingFormatter(logging.Formatter):
    """ Class to format log records.
    """

    def format(self, record):
        """ Format a log record.
        """
        # truncate the name
        name = record.name
        if len(name) > 30:
            name = '{}~{}'.format(name[:5], name[-24:])
        record.name = name
        return super(NameTruncatingFormatter, self).format(record)
