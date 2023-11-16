# -*- coding: utf-8 -*-
"""
Filename: test_async_bots.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 06.11.2023
Last Modified: 06.11.2023

Description:
This file tests for async bots.
"""

from datetime import datetime, timedelta
from logging import ERROR
from random import randint, choice
from secrets import token_hex

import pytest

from src.ablt_python_api.schemas import StatisticsSchema, StatisticItemSchema, StatisticTotalSchema
from tests.test_data import SOME_USER_ID_RANGE, DATE_TEST_PERIOD, KEY_LENGTH


@pytest.mark.asyncio
async def test_async_statistics_whole_statistics(api):
    """
    This method tests for async statistics: get default statistics

    :param api: api fixture
    """
    response = StatisticsSchema.model_validate(await api.get_usage_statistics())
    assert len(response.items) == 1
    assert response.items[0].date.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d")


@pytest.mark.asyncio
async def test_async_statistics_specify_user_id(api):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    """
    response = StatisticsSchema.model_validate(
        await api.get_usage_statistics(
            user_id=choice(
                (f"{randint(-SOME_USER_ID_RANGE, SOME_USER_ID_RANGE)}", token_hex(KEY_LENGTH)),
            )
        )
    )
    assert len(response.items) == 1


@pytest.mark.asyncio
async def test_async_statistics_specify_start_date(api, random_date_generator, days_between_dates):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    :param days_between_dates: days_between_dates fixture
    """
    start_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticsSchema.model_validate(await api.get_usage_statistics(start_date=start_date))
    assert len(response.items) == days_between_dates(start_date)


@pytest.mark.asyncio
async def test_async_statistics_specify_start_date_ahead(api, random_date_generator):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    start_date = random_date_generator(days=DATE_TEST_PERIOD, forward=True)
    response = StatisticsSchema.model_validate(await api.get_usage_statistics(start_date=start_date))
    assert len(response.items) == 0


@pytest.mark.asyncio
async def test_async_statistics_specify_end_date(api, random_date_generator, days_between_dates):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    :param days_between_dates: days_between_dates fixture
    """
    end_date = random_date_generator(days=DATE_TEST_PERIOD, forward=True)
    response = StatisticsSchema.model_validate(await api.get_usage_statistics(end_date=end_date))
    assert len(response.items) == days_between_dates(end_date)


@pytest.mark.asyncio
async def test_async_statistics_specify_end_date_beforehand(api, random_date_generator):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    end_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticsSchema.model_validate(await api.get_usage_statistics(end_date=end_date))
    assert len(response.items) == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_id,start_date,end_date,caplog_error",
    [
        (
            randint(-SOME_USER_ID_RANGE, SOME_USER_ID_RANGE),
            "bad_start_date",
            datetime.now().strftime("%Y-%m-%d"),
            "Error details: {'detail': ["
            "{'loc': ['body', 'start_date'], 'msg': 'invalid date format', 'type': 'value_error.date'}]}",
        ),
        (
            randint(-SOME_USER_ID_RANGE, SOME_USER_ID_RANGE),
            datetime.now().strftime("%Y-%m-%d"),
            "bad_end_date",
            "Error details: "
            "{'detail': [{'loc': ['body', 'end_date'], 'msg': 'invalid date format', 'type': 'value_error.date'}]}",
        ),
        (
            randint(-SOME_USER_ID_RANGE, SOME_USER_ID_RANGE),
            "bad_start_date",
            "bad_end_date",
            "Error details: "
            "{'detail': ["
            "{'loc': ['body', 'start_date'], 'msg': 'invalid date format', 'type': 'value_error.date'}, "
            "{'loc': ['body', 'end_date'], 'msg': 'invalid date format', 'type': 'value_error.date'}]}",
        ),
    ],
    ids=("bad start date", "bad end date", "bad start and end dates"),
)
async def test_async_statistics_with_malformed_payload(api, caplog, user_id, start_date, end_date, caplog_error):
    """
    This method tests for async statistics: get statistics for user_id

    :param api: api fixture
    :param caplog: caplog fixture
    :param user_id: user_id
    :type user_id: str
    :param start_date: start_date
    :type start_date: str
    :param end_date: end_date
    :type end_date: str
    :param caplog_error: caplog_error
    :type caplog_error: str
    """
    caplog.set_level(ERROR)
    response = await api.get_usage_statistics(user_id=user_id, start_date=start_date, end_date=end_date)
    assert response is None
    assert "Request error for " in caplog.text and ": 422" in caplog.text
    assert caplog_error in caplog.text


@pytest.mark.asyncio
async def test_async_statistics_get_item(api, random_date_generator):
    """
    This method tests for async statistics: for a day

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    random_date = random_date_generator(days=DATE_TEST_PERIOD)
    response = StatisticItemSchema.model_validate(
        await api.get_statistics_for_a_day(user_id=token_hex(KEY_LENGTH), date=random_date)
    )
    response = StatisticItemSchema.model_validate(response)
    assert response.date.strftime("%Y-%m-%d") == random_date


@pytest.mark.asyncio
async def test_async_statistics_get_total(api, random_date_generator):
    """
    This method tests for async statistics: for totals

    :param api: api fixture
    :param random_date_generator: random_date_generator fixture
    """
    end_date = (datetime.now() - timedelta(days=randint(0, DATE_TEST_PERIOD))).strftime("%Y-%m-%d")
    start_date = random_date_generator(days=DATE_TEST_PERIOD, end_date=datetime.strptime(end_date, "%Y-%m-%d"))
    response = StatisticTotalSchema.model_validate(
        await api.get_statistics_total(user_id=token_hex(KEY_LENGTH), start_date=start_date, end_date=end_date)
    )
    assert StatisticTotalSchema.model_validate(response)


@pytest.mark.asyncio
async def test_async_statistics_content(api):
    """
    This method tests for async statistics: content

    :param api: api fixture
    """
    date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    response = await api.get_usage_statistics(start_date=date, end_date=date)
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
