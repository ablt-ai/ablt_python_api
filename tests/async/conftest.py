# -*- coding: utf-8 -*-
"""
Filename: conftest.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 05.12.2023

Description:
This file contains pytest fixtures for async API.
"""

import random
from datetime import datetime, timedelta
from os import environ
from typing import Optional

import pytest

from src.ablt_python_api.ablt_api_async import ABLTApi


@pytest.fixture(scope="session")
def api():
    """
    This fixture returns ABLTApi instance.

    :return: ABLTApi instance
    :rtype: ABLTApi
    """
    return ABLTApi(bearer_token=environ["ABLT_BEARER_TOKEN"])


@pytest.fixture()
def random_date_generator():
    """
    This fixture returns a function that generates random date.

    :return: function that generates random date in format %Y-%m-%d
    :rtype: function
    """

    def _generate_random_date(days: int, end_date: Optional[datetime] = None, forward: bool = False):
        """
        This function generates random date.

        :param days: count of days
        :param end_date: end date, by default today
        :param forward: generate date in ahead of today (by default False)
        :return: random date in format %Y-%m-%d
        :rtype: str
        """
        end_date = datetime.now() if end_date is None else end_date
        if forward:
            start_date = end_date
            end_date = end_date + timedelta(days=days)
        else:
            start_date = end_date - timedelta(days=days)

        random_date = start_date + (end_date - start_date) * random.random()

        return random_date.strftime("%Y-%m-%d")

    return _generate_random_date


@pytest.fixture()
def days_between_dates():
    """
    This fixture returns a function that calculates days between two dates.

    :return: function that calculates days between two dates
    :rtype: function
    """

    def _days_between_dates(start_date_str: str, end_date_str: Optional[str] = None):
        """
        This function calculates days between two dates.

        :param start_date_str: start date in format %Y-%m-%d
        :param end_date_str: end date in format %Y-%m-%d
        :return: count of days
        :rtype: int
        """
        end_date_str = datetime.now().strftime("%Y-%m-%d") if end_date_str is None else end_date_str
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        return abs((end_date - start_date).days) + 1

    return _days_between_dates
