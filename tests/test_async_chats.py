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

import pytest
from os import environ
import ssl


from src.ablt_python_api.ablt_api_async import ABLTApi


class TestAsyncChats:
    """This class tests for async chats."""
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE
    api = ABLTApi(bearer_token=environ['BEARER_TOKEN'], ssl_context=sslcontext)

    @pytest.mark.asyncio
    async def test_async_chats_general(self):
        """This method tests for async chats."""
        async_generator = self.api.chat(bot_slug='llama2-13-b-anyscale', prompt='Who is current president of US?',
                                        max_words=3)
        try:
            response = await async_generator.__anext__()
        except StopAsyncIteration:
            response = None
        assert response is not None
