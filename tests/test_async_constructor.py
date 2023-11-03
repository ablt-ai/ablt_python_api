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

import io
import secrets
import ssl
from random import choice
from unittest.mock import patch

from aiohttp import client_exceptions

from src.ablt_python_api.ablt_api_async import ABLTApi


class TestAsyncConstructor:
    """This class tests for async constructor."""
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE

    def test_async_constructor_without_token(self):
        """Test against constructor without token."""
        with self.assertRaises(TypeError):
            ABLTApi()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_async_constructor_default_init_with_any_token(self, mock_stdout):
        """
        Test against constructor with any token.

        :param mock_stdout: mock stdout
        """
        with self.assertLogs('api', level='INFO') as captured:
            ABLTApi(bearer_token=secrets.token_hex(16), ssl_context=self.sslcontext)
        self.assertIn("Logger for API now launched!", mock_stdout.getvalue())
        self.assertIn("ABLT chat API is working like a charm", mock_stdout.getvalue())
        self.assertIn("Logger for API now launched!", captured.output[0])
        self.assertIn("ABLT chat API is working like a charm", captured.output[1])

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_async_constructor_default_init_with_any_token_and_valid_url(self, mock_stdout):
        """
        Test against constructor with any token and valid url.

        :param mock_stdout: mock stdout
        """
        with self.assertLogs('api', level='INFO') as captured:
            ABLTApi(bearer_token=secrets.token_hex(16), base_api_url="https://api.ablt.ai",
                    ssl_context=self.sslcontext)
        self.assertIn("Logger for API now launched!", mock_stdout.getvalue())
        self.assertIn("ABLT chat API is working like a charm", mock_stdout.getvalue())
        self.assertIn("Logger for API now launched!", captured.output[0])
        self.assertIn("ABLT chat API is working like a charm", captured.output[1])

    def test_async_constructor_default_init_with_invalid_url(self):
        """Test against constructor with invalid url."""
        with self.assertRaises(client_exceptions.InvalidURL):
            ABLTApi(bearer_token=secrets.token_hex(16), base_api_url=choice(("", secrets.token_hex(16))),
                    ssl_context=self.sslcontext)

    def test_async_constructor_default_init_with_incorrect_logger(self):
        """Test against constructor with incorrect logger."""
        with self.assertRaises(AttributeError):
            ABLTApi(bearer_token=secrets.token_hex(16), logger=secrets.token_hex(16), ssl_context=self.sslcontext)
