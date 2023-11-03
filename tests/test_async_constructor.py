# -*- coding: utf-8 -*-
"""
Filename: test_async_constructor.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

Description:
This file tests for async constructor.
"""

import secrets
import ssl
from logging import INFO
from random import choice

import pytest
from aiohttp import client_exceptions

from src.ablt_python_api.ablt_api_async import ABLTApi


class TestAsyncConstructor:
    """This class tests for async constructor."""
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE

    def test_async_constructor_without_token(self):
        """Test against constructor without token."""
        with pytest.raises(TypeError):
            ABLTApi()

    def test_async_constructor_default_init_with_any_token(self, caplog):
        """
        Test against constructor with any token.

        :param caplog: caplog pytest fixture
        """
        ABLTApi(bearer_token=secrets.token_hex(16), ssl_context=self.sslcontext)
        assert "Logger for API now launched!" in caplog.text
        assert "ABLT chat API is working like a charm" in caplog.text

    def test_async_constructor_default_init_with_any_token_and_valid_url(self, caplog):
        """
        Test against constructor with any token and valid url.

        :param caplog: caplog pytest fixture
        """
        caplog.set_level(INFO)
        ABLTApi(bearer_token=secrets.token_hex(16), base_api_url="https://api.ablt.ai",
                ssl_context=self.sslcontext)
        assert "Logger for API now launched!" in caplog.text
        assert "ABLT chat API is working like a charm" in caplog.text

    def test_async_constructor_default_init_with_invalid_url(self):
        """Test against constructor with invalid url."""
        with pytest.raises(client_exceptions.InvalidURL):
            ABLTApi(bearer_token=secrets.token_hex(16), base_api_url=choice(("", secrets.token_hex(16))),
                    ssl_context=self.sslcontext)

    def test_async_constructor_default_init_with_incorrect_logger(self):
        """Test against constructor with incorrect logger."""
        with pytest.raises(AttributeError):
            ABLTApi(bearer_token=secrets.token_hex(16), logger=secrets.token_hex(16), ssl_context=self.sslcontext)
