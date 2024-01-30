# -*- coding: utf-8 -*-
"""
Filename: test_async_other.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 06.11.2023
Last Modified: 30.01.2024

Description:
This file tests for async other helper stuff.
"""

from secrets import token_hex

import pytest
from aiohttp import client_exceptions

from src.ablt_python_api.ablt_api_async import ABLTApi
from tests.test_data import KEY_LENGTH


test_api = ABLTApi(bearer_token=token_hex(KEY_LENGTH))


@pytest.mark.asyncio
async def test_async_other_health_check(caplog):
    """
    This method tests for async other: health check.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    await test_api.health_check()
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.asyncio
async def test_async_other_update_api(caplog):
    """
    This method tests for async other: update api.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    await test_api.update_api()
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.asyncio
async def test_async_other_set_bearer_token(caplog):
    """
    This method tests for async other: bearer token.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    new_token = token_hex(KEY_LENGTH)
    await test_api.set_bearer_token(new_token)
    assert test_api.get_bearer_token() == new_token
    assert "ABLT chat API is working like a charm" not in caplog.text


@pytest.mark.asyncio
async def test_async_other_set_bearer_token_instant(caplog):
    """
    This method tests for async other: bearer token.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    new_token = token_hex(KEY_LENGTH)
    await test_api.set_bearer_token(new_token, instant_update=True)
    assert test_api.get_bearer_token() == new_token
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.asyncio
async def test_async_other_set_base_api_url(caplog):
    """
    This method tests for async other: base api url.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    url = token_hex(KEY_LENGTH)
    await test_api.set_base_api_url(url)
    assert test_api.get_base_api_url() == url
    assert "ABLT chat API is working like a charm" not in caplog.text


@pytest.mark.asyncio
async def test_async_other_set_base_api_url_instant(caplog):
    """
    This method tests for async other: base api url.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    url = token_hex(KEY_LENGTH)
    with pytest.raises(client_exceptions.InvalidURL):
        await test_api.set_base_api_url(url, instant_update=True)
    assert test_api.get_base_api_url() == url
    assert "ABLT chat API is working like a charm" not in caplog.text


@pytest.mark.asyncio
async def test_async_other_update_api_info_base_url(caplog):
    """
    This method tests for async other: update api info.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    old_token = test_api.get_bearer_token()
    await test_api.update_api_info(new_base_api_url="https://api.ablt.ai")
    assert "ABLT chat API is working like a charm" in caplog.text
    assert test_api.get_base_api_url() == "https://api.ablt.ai"
    assert test_api.get_bearer_token() == old_token


@pytest.mark.asyncio
async def test_async_other_update_api_info_bearer_token(caplog):
    """
    This method tests for async other: update api info.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    new_token = token_hex(KEY_LENGTH)
    await test_api.update_api_info(new_bearer_token=new_token)
    assert "ABLT chat API is working like a charm" in caplog.text
    assert test_api.get_bearer_token() == new_token
    assert test_api.get_base_api_url() == "https://api.ablt.ai"


@pytest.mark.asyncio
async def test_async_other_update_api_info_both(caplog):
    """
    This method tests for async other: update api info.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level("INFO")
    await test_api.set_base_api_url(token_hex(KEY_LENGTH))
    old_api_url = test_api.get_base_api_url()
    new_token = token_hex(KEY_LENGTH)
    await test_api.update_api_info(new_base_api_url="https://api.ablt.ai", new_bearer_token=new_token)
    assert "ABLT chat API is working like a charm" in caplog.text
    assert test_api.get_bearer_token() == new_token
    assert test_api.get_base_api_url() == "https://api.ablt.ai"
    assert test_api.get_base_api_url() != old_api_url


@pytest.mark.asyncio
async def test_async_other_get_base_api_url():
    """This method tests for async other: get base api url."""
    assert test_api.get_base_api_url() == "https://api.ablt.ai"


@pytest.mark.asyncio
async def test_async_other_get_bearer_token():
    """This method tests for async other: get bearer token."""
    assert test_api.get_bearer_token() is not None


@pytest.mark.asyncio
async def test_async_other_set_logger():
    """This method tests for async other: set logger."""
    test_api.set_logger(new_logger=token_hex(KEY_LENGTH))
    with pytest.raises(AttributeError):
        await test_api.health_check()
