# -*- coding: utf-8 -*-
"""
Filename: test_sync_constructor.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 20.11.2023
Last Modified: 05.12.2023

Description:
This file tests for sync constructor.
"""
from logging import INFO
from os import environ
from secrets import token_hex

import pytest

from src.ablt_python_api.ablt_api_sync import ABLTApi
from tests.test_data import KEY_LENGTH


@pytest.mark.sync
def test_sync_constructor_without_token():
    """Test against constructor without token."""
    bearer_token = environ["ABLT_BEARER_TOKEN"]
    environ["ABLT_BEARER_TOKEN"] = ""
    with pytest.raises(TypeError):
        ABLTApi()
    environ["ABLT_BEARER_TOKEN"] = bearer_token


@pytest.mark.sync
def test_sync_constructor_with_env_token(caplog):
    """
    Test against constructor without token.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level(INFO)
    ABLTApi()
    assert "Logger for API now launched!" in caplog.text
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.sync
def test_sync_constructor_default_init_with_any_token(caplog):
    """
    Test against constructor with any token.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level(INFO)
    ABLTApi(
        bearer_token=token_hex(KEY_LENGTH),
    )
    assert "Logger for API now launched!" in caplog.text
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.sync
def test_sync_constructor_default_init_with_any_token_and_valid_url(caplog):
    """
    Test against constructor with any token and valid url.

    :param caplog: caplog pytest fixture
    """
    caplog.set_level(INFO)
    ABLTApi(
        bearer_token=token_hex(KEY_LENGTH),
        base_api_url="https://api.ablt.ai",
    )
    assert "Logger for API now launched!" in caplog.text
    assert "ABLT chat API is working like a charm" in caplog.text


@pytest.mark.sync
def test_sync_constructor_default_init_with_invalid_url():
    """Test against constructor with invalid url."""
    with pytest.raises(ConnectionError):
        ABLTApi(
            bearer_token=token_hex(KEY_LENGTH),
            base_api_url=f"https://{token_hex(KEY_LENGTH)}",
        )


@pytest.mark.sync
@pytest.mark.new
def test_sync_constructor_default_init_with_empty_url():
    """Test against constructor with invalid url."""
    with pytest.raises(ConnectionError):
        ABLTApi(
            bearer_token=token_hex(KEY_LENGTH),
            base_api_url="",
        )


@pytest.mark.sync
@pytest.mark.new
def test_sync_constructor_default_init_with_incorrect_logger():
    """Test against constructor with incorrect logger."""
    with pytest.raises(AttributeError):
        ABLTApi(
            bearer_token=token_hex(KEY_LENGTH),
            logger=token_hex(KEY_LENGTH),
        )
