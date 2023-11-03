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

from os import environ
from random import choice

import pytest

from src.ablt_python_api.ablt_api_async import ABLTApi
from tests.test_data import sample_questions, unique_models, sslcontext


@pytest.fixture
def api():
    """This fixture returns ABLTApi instance."""
    return ABLTApi(bearer_token=environ["BEARER_TOKEN"], ssl_context=sslcontext)


@pytest.mark.asyncio
@pytest.mark.parametrize("bot_slug", unique_models, ids=unique_models)
@pytest.mark.parametrize("stream", (False, True), ids=("not_stream", "stream"))
async def test_async_chats_unique_models(api, bot_slug, stream):
    """
    This method tests for async chats (with/without stream) for unique models.

    :param bot_slug: bot slug
    """
    max_words = 3
    async_generator = api.chat(
        bot_slug=bot_slug, prompt=choice(sample_questions), max_words=max_words, stream=stream
    )
    try:
        response = await async_generator.__anext__()
    except StopAsyncIteration:
        response = None
    assert response is not None


@pytest.mark.asyncio
async def test_async_chats_tbd1():
    """This method tests for async chats."""
    assert True


@pytest.mark.asyncio
async def test_async_chats_tbd2():
    """This method tests for async chats."""
    assert True
