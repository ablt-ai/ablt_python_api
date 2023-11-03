# -*- coding: utf-8 -*-
"""
Filename: conftest.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

Description:
This file contains pytest fixtures.
"""

from os import environ

import pytest

from src.ablt_python_api.ablt_api_async import ABLTApi
from .test_data import sslcontext


@pytest.fixture(scope="session")
def api():
    """
    This fixture returns ABLTApi instance.

    :return: ABLTApi instance
    :rtype: ABLTApi
    """
    return ABLTApi(bearer_token=environ["BEARER_TOKEN"], ssl_context=sslcontext)
