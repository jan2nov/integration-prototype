# coding: utf-8
""" Logging aggregator service for ZeroMQ Python Logging messages.

.. moduleauthor:: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import logging

from . import app

# Define a logging formatter and handler.
FORMAT = logging.Formatter("> [%(levelname).1s] %(message)-50s (%(name)s:L%(lineno)i)")
HANDLER = logging.StreamHandler()
HANDLER.setFormatter(FORMAT)

# Set the default SIP logging handler and logging level.
SIP = logging.getLogger('sip')
SIP.addHandler(HANDLER)
SIP.setLevel(logging.DEBUG)

# Set the default Flask logging handler and level
FLASK_LOG = logging.getLogger('werkzeug')
FLASK_LOG.addHandler(HANDLER)
FLASK_LOG.setLevel(logging.WARNING)

# Start the app
app.main()
