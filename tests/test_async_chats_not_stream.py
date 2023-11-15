# -*- coding: utf-8 -*-
"""
Filename: test_async_chats_not_stream.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 15.11.2023

Description:
This file tests for async chats (non-streaming mode).
"""
# pylint: disable=R0801
from logging import ERROR
from random import choice, randint
from secrets import token_hex

import pytest

from src.ablt_python_api.schemas import BotSchema, StatisticsSchema
from tests.test_data import sample_questions, MIN_WORDS, sample_messages, LANGUAGES, language_questions


async def get_full_response(async_generator):
    """
    This method gets full response from async generator

    :param async_generator: async generator
    :return: str, full response
    """
    try:
        response = await async_generator.__anext__()  # pylint: disable=C2801
    except StopAsyncIteration:
        response = None
    return response


@pytest.mark.asyncio
async def test_async_chats_not_stream_missed_bot_info(api, caplog):
    """
    This method tests for async chat missed any bot info

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    async_generator = api.chat(prompt=choice(sample_questions), max_words=MIN_WORDS, stream=False)
    response = await get_full_response(async_generator)
    assert response is None and "Error: Only one param is required ('bot_slug' or 'bot_uid')" in caplog.text


@pytest.mark.asyncio
async def test_async_chats_not_stream_both_bot_ids_provided(api, caplog):
    """
    This method tests for async chat use messages with prompt at same time

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(
        bot_uid=bot.uid,
        bot_slug=bot.slug,
        prompt=choice(sample_questions),
        max_words=MIN_WORDS,
        stream=False,
    )
    response = await get_full_response(async_generator)
    assert response is None and "Error: Only one param is required ('bot_slug' or 'bot_uid')" in caplog.text


@pytest.mark.asyncio
async def test_async_chats_not_stream_bot_selection_by_slug(api):
    """
    This method tests for async chatbot selection by slug

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(bot_slug=bot.slug, prompt="What is your name?", max_words=MIN_WORDS, stream=False)
    response = await get_full_response(async_generator)
    assert bot.name.replace(" Bot", "").replace(" Template", "").lower() in response.lower()


@pytest.mark.asyncio
async def test_async_chats_not_stream_bot_selection_by_uid(api):
    """
    This method tests for async chatbot selection by uid

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(bot_uid=bot.uid, prompt="What is your name?", max_words=MIN_WORDS, stream=False)
    response = await get_full_response(async_generator)
    assert bot.name.replace(" Bot", "").replace(" Template", "").lower() in response.lower()


@pytest.mark.asyncio
async def test_async_chats_not_stream_missed_input(api, caplog):
    """
    This method tests for async chat use messages instead of prompt

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(bot_uid=bot.uid, max_words=MIN_WORDS, stream=False)
    response = await get_full_response(async_generator)
    assert response is None and "Error: Only one param is required ('prompt' or 'messages')" in caplog.text


@pytest.mark.asyncio
async def test_async_chats_not_stream_both_input_provided(api, caplog):
    """
    This method tests for async chat use messages with prompt at same time

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(
        bot_uid=bot.uid,
        messages=choice(sample_messages),
        prompt=choice(sample_questions),
        max_words=MIN_WORDS,
        stream=False,
    )
    response = await get_full_response(async_generator)
    assert response is None and "Error: Only one param is required ('prompt' or 'messages')" in caplog.text


@pytest.mark.asyncio
async def test_async_chats_not_stream_use_messages(api):
    """
    This method tests for async chat use messages instead of prompt

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    messages = choice(sample_messages)
    async_generator = api.chat(bot_uid=bot.uid, messages=messages["message"], max_words=MIN_WORDS, stream=False)
    response = await get_full_response(async_generator)
    assert messages["expected_answer"] in response


@pytest.mark.xfail(reason="BUG: Statistics always returns 0")
@pytest.mark.asyncio
async def test_async_chats_not_stream_specify_user(api):
    """
    This method tests for async chat specify user

    :param api: api fixture (returns ABLTApi instance)
    """
    user_id = token_hex(MIN_WORDS)
    user_usage = int(
        StatisticsSchema.model_validate(await api.get_usage_statistics(user_id=user_id)).total.total_tokens
    )
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(
        bot_uid=bot.uid,
        prompt=choice(sample_questions),
        max_words=MIN_WORDS,
        stream=False,
        user=user_id,
    )
    response = await get_full_response(async_generator)
    updated_usage = int(
        StatisticsSchema.model_validate(await api.get_usage_statistics(user_id=user_id)).total.total_tokens
    )
    assert response is not None
    assert updated_usage > user_usage


@pytest.mark.asyncio
@pytest.mark.parametrize("language", LANGUAGES, ids=LANGUAGES)
async def test_async_chats_not_stream_check_language(api, language):
    """
    This method tests for async chat specify user and messages

    :param api: api fixture (returns ABLTApi instance)
    :param language: language to test
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    question = choice(language_questions)
    async_generator = api.chat(
        bot_uid=bot.uid,
        prompt=question["question"][language],
        language=language,
        max_words=MIN_WORDS,
        stream=False,
    )
    response = await get_full_response(async_generator)
    assert question["answer"][language] in response.lower()


@pytest.mark.xfail(reason="RESEARCH: Token to word recalculation gives different results")
@pytest.mark.asyncio
async def test_async_chats_not_stream_max_words(api):
    """
    This method tests for async chat max words

    :param api: api fixture (returns ABLTApi instance)
    """
    max_words = randint(3, 10)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in await api.get_bots()])
    async_generator = api.chat(
        bot_uid=bot.uid,
        prompt=choice(sample_questions),
        max_words=max_words,
        stream=False,
    )
    response = await get_full_response(async_generator)
    assert len(response.split()) <= max_words
