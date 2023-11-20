# -*- coding: utf-8 -*-
"""
Filename: test_sync_chats_stream.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 20.11.2023
Last Modified: 20.11.2023

Description:
This file tests for sync chats (streaming mode).
"""
# pylint: disable=R0801
from logging import ERROR
from random import choice, randint

import pytest

from src.ablt_python_api.schemas import BotSchema, StatisticsSchema
from src.ablt_python_api.utils.exceptions import DoneException
from tests.test_data import (
    sample_questions,
    sample_messages,
    language_questions,
    wrong_chat_params,
    LANGUAGES,
    LOWER_USER_ID,
    MIN_WORDS,
    UPPER_USER_ID,
)


def get_full_response(sync_generator):
    """
    This method gets full response from sync generator

    :param sync_generator:
    :return: str, full response
    """
    full_response = []
    try:
        for response in sync_generator:
            assert response is not None
            full_response.append(response)
    except (StopIteration, DoneException):
        pass
    return "".join(full_response) if len(full_response) > 0 else None


@pytest.mark.sync
def test_sync_chats_stream_missed_bot_info(api, caplog):
    """
    This method tests for sync chat missed any bot info

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    sync_generator = api.chat(prompt=choice(sample_questions), max_words=MIN_WORDS, stream=True)
    response = get_full_response(sync_generator)
    assert response is None and "Error: Only one param is required ('bot_slug' or 'bot_uid')" in caplog.text


@pytest.mark.sync
def test_sync_chats_stream_both_bot_ids_provided(api, caplog):
    """
    This method tests for sync chat use messages with prompt at same time

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(
        bot_uid=bot.uid, bot_slug=bot.slug, prompt=choice(sample_questions), max_words=MIN_WORDS, stream=True
    )
    response = get_full_response(sync_generator)
    assert response is None and "Error: Only one param is required ('bot_slug' or 'bot_uid')" in caplog.text


@pytest.mark.sync
def test_sync_chats_stream_bot_selection_by_slug(api):
    """
    This method tests for sync chatbot selection by slug

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(
        bot_slug=bot.slug, prompt="What is your name? Answer just one word (name).", max_words=MIN_WORDS, stream=True
    )
    response = get_full_response(sync_generator)
    assert bot.name.replace(" Bot", "").replace(" Template", "").lower() in response.lower()


@pytest.mark.sync
def test_sync_chats_stream_bot_selection_by_uid(api):
    """
    This method tests for sync chatbot selection by uid

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(bot_uid=bot.uid, prompt="What is your name?", max_words=MIN_WORDS, stream=True)
    response = get_full_response(sync_generator)
    assert bot.name.replace(" Bot", "").replace(" Template", "").lower() in response.lower()


@pytest.mark.sync
def test_sync_chats_stream_missed_input(api, caplog):
    """
    This method tests for sync chat use messages instead of prompt

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(bot_uid=bot.uid, max_words=MIN_WORDS, stream=True)
    response = get_full_response(sync_generator)
    assert response is None and "Error: Only one param is required ('prompt' or 'messages')" in caplog.text


@pytest.mark.sync
def test_sync_chats_stream_both_input_provided(api, caplog):
    """
    This method tests for sync chat use messages with prompt at same time

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    """
    caplog.set_level(ERROR)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(
        bot_uid=bot.uid,
        messages=choice(sample_messages),
        prompt=choice(sample_questions),
        max_words=MIN_WORDS,
        stream=True,
    )
    response = get_full_response(sync_generator)
    assert response is None and "Error: Only one param is required ('prompt' or 'messages')" in caplog.text


@pytest.mark.sync
def test_sync_chats_stream_use_messages(api):
    """
    This method tests for sync chat use messages instead of prompt

    :param api: api fixture (returns ABLTApi instance)
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    messages = choice(sample_messages)
    sync_generator = api.chat(bot_uid=bot.uid, messages=messages["message"], max_words=MIN_WORDS, stream=True)
    response = get_full_response(sync_generator)
    if response is not None:
        assert messages["expected_answer"] in response
    else:
        raise AssertionError("Response is None")


@pytest.mark.sync
def test_sync_chats_stream_specify_user(api):
    """
    This method tests for sync chat specify user

    :param api: api fixture (returns ABLTApi instance)
    """
    user_id = randint(LOWER_USER_ID, UPPER_USER_ID)
    user_usage = int(StatisticsSchema.model_validate(api.get_usage_statistics(user_id=user_id)).total.total_tokens)
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(
        bot_uid=bot.uid,
        prompt=choice(sample_questions),
        max_words=MIN_WORDS,
        stream=True,
        user_id=user_id,
    )
    response = get_full_response(sync_generator)
    updated_usage = int(StatisticsSchema.model_validate(api.get_usage_statistics(user_id=user_id)).total.total_tokens)
    assert response is not None
    assert updated_usage > user_usage


@pytest.mark.sync
@pytest.mark.parametrize("language", LANGUAGES, ids=LANGUAGES)
def test_sync_chats_stream_check_language(api, language):
    """
    This method tests for sync chat specify user and messages

    :param api: api fixture (returns ABLTApi instance)
    :param language: language to test
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    question = choice(language_questions)
    sync_generator = api.chat(
        bot_uid=bot.uid, prompt=question["question"][language], language=language, max_words=MIN_WORDS, stream=True
    )
    response = get_full_response(sync_generator)
    assert question["answer"][language] in response.lower()


@pytest.mark.sync
def test_sync_chats_stream_max_words(api):
    """
    This method tests for sync chat max words

    :param api: api fixture (returns ABLTApi instance)
    """
    max_words = randint(3, 10)
    tolerance = 1  # tolerance for tokens to words conversion
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    sync_generator = api.chat(bot_uid=bot.uid, prompt=choice(sample_questions), max_words=max_words, stream=True)
    response = get_full_response(sync_generator)
    assert len(response.split()) <= (max_words + tolerance)


@pytest.mark.sync
@pytest.mark.parametrize("params", wrong_chat_params, ids=[item["id"] for item in wrong_chat_params])
def test_sync_chats_not_stream_wrong_option(api, caplog, params):
    """
    This method tests for sync chat wrong options

    :param api: api fixture (returns ABLTApi instance)
    :param caplog: caplog pytest fixture
    :param params: params for test
    """
    bot = choice([BotSchema.model_validate(bot_dict) for bot_dict in api.get_bots()])
    bot_uid = bot.uid if "bot_slug" not in params.keys() else None
    prompt = choice(sample_questions) if "prompt" not in params.keys() else params["prompt"]
    prompt = prompt if "messages" not in params.keys() else None
    sync_generator = api.chat(
        bot_uid=bot_uid if "bot_uid" not in params.keys() else params["bot_uid"],
        bot_slug=None if "bot_slug" not in params.keys() else params["bot_slug"],
        prompt=None if "messages" in params.keys() else prompt,
        messages=params["messages"] if "messages" in params.keys() else None,
        use_search=params["use_search"] if "use_search" in params.keys() else False,
        max_words=MIN_WORDS,
        stream=False,
    )
    response = get_full_response(sync_generator)
    assert response is None, f"Response is {response}"
    assert all(message in caplog.text for message in params["expected"]), "Not all messages were found in caplog"


@pytest.mark.sync
def test_sync_chats_stream_use_search(api):
    """
    This method tests for sync chat use web search

    :param api: api fixture (returns ABLTApi instance)
    """
    return api  # TBD
