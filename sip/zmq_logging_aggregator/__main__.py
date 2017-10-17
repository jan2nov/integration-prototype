# coding: utf-8
""" Logging aggregator for ZeroMQ Python Logging messages.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging

from . import app
# from .lib.formatter import NameTruncatingFormatter

# Define a logging formatter and handler.
# FORMAT = NameTruncatingFormatter("> %(name)-30s | %(message)s")
FORMAT = logging.Formatter("= %(name).40s | %(message)s")
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMAT)

# Set the default SIP / ZLA logging handler and level
SIP = logging.getLogger('')
SIP.addHandler(HANDLER)
SIP.setLevel(logging.DEBUG)

# Set the default Flask logging handler and level
FLASK_LOG = logging.getLogger('werkzeug')
FLASK_LOG.addHandler(HANDLER)
FLASK_LOG.setLevel(logging.ERROR)


# Start the app
app.main()
