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

import random
from datetime import datetime, timedelta
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
    return ABLTApi(bearer_token=environ["ABLT_BEARER_TOKEN"], ssl_context=sslcontext)


@pytest.fixture()
def random_date_generator():
    """
    This fixture returns a function that generates random date.

    :return: function that generates random date in format %Y-%m-%d
    :rtype: function
    """

    def _generate_random_date(days: int, end_date: datetime = datetime.now(), forward: bool = False):
        """
        This function generates random date.

        :param days: count of days
        :param end_date: end date, by default today
        :param forward: generate date in ahead of today (by default False)
        :return: random date in format %Y-%m-%d
        :rtype: str
        """
        if forward:
            start_date = end_date
            end_date = end_date + timedelta(days=days)
        else:
            start_date = end_date - timedelta(days=days)

        random_date = start_date + (end_date - start_date) * random.random()
        formatted_random_date = random_date.strftime("%Y-%m-%d")

        return formatted_random_date

    return _generate_random_date


@pytest.fixture()
def days_between_dates():
    """
    This fixture returns a function that calculates days between two dates.

    :return: function that calculates days between two dates
    :rtype: function
    """

    def _days_between_dates(start_date_str: str, end_date_str: str = datetime.now().strftime("%Y-%m-%d")):
        """
        This function calculates days between two dates.

        :param start_date_str: start date in format %Y-%m-%d
        :param end_date_str: end date in format %Y-%m-%d
        :return: count of days
        :rtype: int
        """
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        return abs((end_date - start_date).days) + 1

    return _days_between_dates
