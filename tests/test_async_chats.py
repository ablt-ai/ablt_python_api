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

from random import choice

import pytest

from src.ablt_python_api.utils.exceptions import DoneException
from tests.test_data import sample_questions, unique_models, MIN_WORDS


@pytest.mark.asyncio
@pytest.mark.parametrize("bot_slug", unique_models, ids=unique_models)
async def test_async_chats_unique_models_not_stream(api, bot_slug):
    """
    This method tests for async chats (with/without stream) for unique models.

    :param api: api fixture
    :param bot_slug: bot slug
    """
    max_words = 3
    async_generator = api.chat(bot_slug=bot_slug, prompt=choice(sample_questions), max_words=max_words, stream=False)
    try:
        response = await async_generator.anext()
    except StopAsyncIteration:
        response = None
    assert response is not None


@pytest.mark.asyncio
@pytest.mark.parametrize("bot_slug", unique_models, ids=unique_models)
async def test_async_chats_unique_models_stream(api, bot_slug):
    """
    This method tests for async chats (with/without stream) for unique models.

    :param api: api fixture
    :param bot_slug: bot slug
    """
    max_words = MIN_WORDS
    async_generator = api.chat(bot_slug=bot_slug, prompt=choice(sample_questions), max_words=max_words, stream=True)
    full_response = []
    try:
        async for response in async_generator:
            assert response is not None
            full_response.append(response)
    except (StopAsyncIteration, DoneException):
        pass
    assert len(full_response) > 0


@pytest.mark.asyncio
async def test_async_chats_tbd1():
    """This method tests for async chats."""
    assert True


@pytest.mark.asyncio
async def test_async_chats_tbd2():
    """This method tests for async chats."""
    assert True
