# coding=utf-8
""" ZMQ logging aggregator configuration functions

This module provides methods used by the logging aggregator service to
configure the logger.

.. moduleauthor: Ben Mort <benjamin.mort@oerc.ox.ac.uk>
"""
import json
import logging
import logging.config
import os

import yaml


def load_config_file(config_file):
    """" Load a YAML or JSON logging config file.

    Args:
        config_file (str): Path of the logging configuration file

    Returns:
        string, Configuration dictionary.
    """
    log = logging.getLogger(__name__)
    _, extension = os.path.splitext(config_file)
    with open(config_file) as file:
        if extension.lower() in ['.yaml', '.yml']:
            try:
                return yaml.load(file)
            except yaml.YAMLError:
                log.error('Unable to load YAML logging configuration')
                raise
        elif extension.lower() in ['.json']:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                log.error('Unable to load JSON logging configuration')
                raise
        else:
            log.error('Unrecognised extension.')
            return None


def load_logging_config(config_file):
    """ Load a YAML or JSON logging configuration file.

    Args:
        config_file (str): Path of the logging configuration file
    """
    log = logging.getLogger(__name__)
    config_dict = load_config_file(config_file)
    # log.debug(json.dumps(config_dict, indent=2))
    logging.config.dictConfig(config_dict)
    log.debug('Logging configuration updated.')


def configure_logger(config_file, host=None):
    """ Configure the Python logger for use with SIP

    Sets a logging LogRecord factory method which adds custom fields into the
    LogRecord object.

    Args:
        config_file (string): Path of the logging configuration file
        host (string): Hostname of the logging aggregator.
    """
    config_dict = load_config_file(config_file)
    if host:
        config_dict['handlers']['zmq']['host'] = host
    logging.config.dictConfig(config_dict)
    # print(json.dumps(config_dict, indent=2))
