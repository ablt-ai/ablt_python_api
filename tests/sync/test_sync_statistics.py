# -*- coding: utf-8 -*-
"""
Filename: test_sync_statistics.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 20.11.2023
Last Modified: 20.11.2023

Description:
This file tests for sync bots.
"""

from datetime import datetime, timedelta
from logging import ERROR
from random import randint
from secrets import token_hex

import pytest

from src.ablt_python_api.schemas import StatisticsSchema, StatisticItemSchema, StatisticTotalSchema
from tests.test_data import (
    LOWER_USER_ID,
    UPPER_USER_ID,
    DATE_TEST_PERIOD,
    KEY_LENGTH,
    malformed_statistics,
    malformed_statistics_ids,
)


@pytest.mark.sync
def test_sync_statistics_whole_statistics(api):
    """
    This method tests for sync statistics: get default statistics

    :param api: api fixture
    """
    response = StatisticsSchema.model_validate(api.get_usage_statistics())
    assert len(response.items) == 1
    assert response.items[0].date.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d")


@pytest.mark.sync
def test_sync_statistics_specify_user_id(api):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    """
    response = StatisticsSchema.model_validate(api.get_usage_statistics(user_id=randint(LOWER_USER_ID, UPPER_USER_ID)))
    assert len(response.items) == 1


@pytest.mark.sync
def test_sync_statistics_specify_start_date(api, random_date_generator, days_between_dates):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    :param days_between_dates: days_between_dates fixture
    """
    start_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticsSchema.model_validate(api.get_usage_statistics(start_date=start_date))
    assert len(response.items) == days_between_dates(start_date)


@pytest.mark.sync
def test_sync_statistics_specify_start_date_ahead(api, random_date_generator):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    start_date = random_date_generator(days=DATE_TEST_PERIOD, forward=True)
    response = StatisticsSchema.model_validate(api.get_usage_statistics(start_date=start_date))
    assert len(response.items) == 0


@pytest.mark.sync
def test_sync_statistics_specify_end_date(api, random_date_generator, days_between_dates):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    :param days_between_dates: days_between_dates fixture
    """
    end_date = random_date_generator(days=DATE_TEST_PERIOD, forward=True)
    response = StatisticsSchema.model_validate(api.get_usage_statistics(end_date=end_date))
    assert len(response.items) == days_between_dates(end_date)


@pytest.mark.sync
def test_sync_statistics_specify_end_date_beforehand(api, random_date_generator):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    end_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticsSchema.model_validate(api.get_usage_statistics(end_date=end_date))
    assert len(response.items) == 0


@pytest.mark.sync
@pytest.mark.parametrize("user_id,start_date,end_date,caplog_error", malformed_statistics, ids=malformed_statistics_ids)
def test_sync_statistics_with_malformed_payload(api, caplog, user_id, start_date, end_date, caplog_error):
    """
    This method tests for sync statistics: get statistics for user_id

    :param api: api fixture
    :param caplog: caplog fixture
    :param user_id: user_id
    :type user_id: int
    :param start_date: start_date
    :type start_date: str
    :param end_date: end_date
    :type end_date: str
    :param caplog_error: caplog_error
    :type caplog_error: str
    """
    caplog.set_level(ERROR)
    response = api.get_usage_statistics(user_id=user_id, start_date=start_date, end_date=end_date)
    assert response is None
    assert "Request error: 422, x-request-id: " in caplog.text
    assert caplog_error in caplog.text


@pytest.mark.sync
def test_sync_statistics_get_item(api, random_date_generator):
    """
    This method tests for sync statistics: for a day

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    random_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticItemSchema.model_validate(
        api.get_statistics_for_a_day(user_id=randint(LOWER_USER_ID, UPPER_USER_ID), date=random_date)
    )
    response = StatisticItemSchema.model_validate(response)
    assert response.date.strftime("%Y-%m-%d") == random_date


@pytest.mark.sync
def test_sync_statistics_get_total(api, random_date_generator):
    """
    This method tests for sync statistics: for totals

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    end_date = (datetime.now() - timedelta(days=randint(0, DATE_TEST_PERIOD))).strftime("%Y-%m-%d")
    start_date = random_date_generator(days=DATE_TEST_PERIOD, end_date=datetime.strptime(end_date, "%Y-%m-%d"))
    response = StatisticTotalSchema.model_validate(
        api.get_statistics_total(
            user_id=randint(LOWER_USER_ID, UPPER_USER_ID), start_date=start_date, end_date=end_date
        )
    )
    assert StatisticTotalSchema.model_validate(response)


@pytest.mark.sync
def test_sync_statistics_content(api):
    """
    This method tests for sync statistics: content

    :param api: api fixture
    """
    date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = api.get_usage_statistics(start_date=date, end_date=date)
    expected = {
        "total": {
            "original_tokens": 0,
            "enchancement_tokens": 0,
            "response_tokens": 0,
            "total_tokens": 0,
            "original_words": 0,
            "enchancement_words": 0,
            "response_words": 0,
            "total_words": 0,
        },
        "items": [
            {
                "original_tokens": 0,
                "enchancement_tokens": 0,
                "response_tokens": 0,
                "total_tokens": 0,
                "original_words": 0,
                "enchancement_words": 0,
                "response_words": 0,
                "total_words": 0,
                "date": date,
            }
        ],
    }
    assert response == expected


@pytest.mark.sync
def test_sync_statistics_wrong_user_id_usage(api, caplog):
    """
    This method tests for sync statistics: wrong user_id for usage

    :param api: api fixture
    """
    response = api.get_usage_statistics(user_id=token_hex(KEY_LENGTH))
    assert response is None
    assert "Error: user_id should be int" in caplog.text


@pytest.mark.sync
def test_sync_statistics_wrong_user_id_day(api, caplog):
    """
    This method tests for sync statistics: wrong user_id for a day

    :param api: api fixture
    """
    response = api.get_statistics_for_a_day(user_id=token_hex(KEY_LENGTH))
    assert response is None
    assert "Error: user_id should be int" in caplog.text


@pytest.mark.sync
def test_sync_statistics_wrong_user_id_total(api, caplog):
    """
    This method tests for sync statistics: wrong user_id for total

    :param api: api fixture
    """
    response = api.get_statistics_total(user_id=token_hex(KEY_LENGTH))
    assert response is None
    assert "Error: user_id should be int" in caplog.text
