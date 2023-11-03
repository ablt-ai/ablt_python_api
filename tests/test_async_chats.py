# -*- coding: utf-8 -*-
"""
Filename: test_async_constructor.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

Description:
This file tests for async chats.
"""

import ssl
from os import environ
from random import choice

import pytest

from src.ablt_python_api.ablt_api_async import ABLTApi
from tests.test_data import sample_questions, unique_models


class TestAsyncChats:
    """This class tests for async chats."""
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE
    api = ABLTApi(bearer_token=environ['BEARER_TOKEN'], ssl_context=sslcontext)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("bot_slug", unique_models)
    async def test_async_chats_general(self, bot_slug):
        """
        This method tests for async chats.

        :param bot_slug: bot slug
        """
        max_words = 3
        async_generator = self.api.chat(bot_slug=bot_slug, prompt=choice(sample_questions), max_words=max_words,
                                        stream=False)
        try:
            response = await async_generator.__anext__()
        except StopAsyncIteration:
            response = None
        print(response)
        assert response is not None
