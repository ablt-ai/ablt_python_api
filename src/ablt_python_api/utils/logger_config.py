"""
Filename: logger_config.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

Description:
This file contains an configuration for loggers.
"""

import logging
import os
import sys
from typing import Optional


def setup_logger(name: str, log_file: Optional[str] = None, level: int = logging.DEBUG):
    """
    Function to setup as many loggers as you want

    :param name: logger name
    :type name: str
    :param log_file: log file name
    :type log_file: str
    :param level: default logging level. By default - DEBUG
    :type level: int
    :return: logger
    :rtype: logging.Logger
    """
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not is_heroku_environment() and log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def is_heroku_environment():
    """
    Check current env - are we on Heroku or not

    :return: True is current environment is Heroku, otherwise - False.
    :rtype: bool
    """
    return "DYNO" in os.environ and "PORT" in os.environ
