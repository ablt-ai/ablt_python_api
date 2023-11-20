# -*- coding: utf-8 -*-
"""
Filename: test_sync_unique_models.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 20.11.2023
Last Modified: 20.11.2023

Description:
This file tests for sync chats (unique models).
"""
from random import choice

import pytest

from src.ablt_python_api.utils.exceptions import DoneException
from tests.test_data import sample_questions, MIN_WORDS, unique_models


@pytest.mark.skip
@pytest.mark.sync
@pytest.mark.parametrize("bot_slug", unique_models, ids=unique_models)
def test_sync_unique_models_not_stream(api, bot_slug):
    """
    This method tests for sync chats (with/without stream) for unique models.

    :param api: api fixture
    :param bot_slug: bot slug
    """
    sync_generator = api.chat(bot_slug=bot_slug, prompt=choice(sample_questions), max_words=MIN_WORDS, stream=False)
    try:
        response = sync_generator.__anext__()  # pylint: disable=C2801
    except StopIteration:
        response = None
    assert response is not None


@pytest.mark.skip
@pytest.mark.sync
@pytest.mark.parametrize("bot_slug", unique_models, ids=unique_models)
def test_sync_chats_unique_models_stream(api, bot_slug):
    """
    This method tests for sync chats (with/without stream) for unique models.

    :param api: api fixture (returns ABLTApi instance)
    :param bot_slug: bot slug
    """
    sync_generator = api.chat(bot_slug=bot_slug, prompt=choice(sample_questions), max_words=MIN_WORDS, stream=True)
    full_response = []
    try:
        for response in sync_generator:
            assert response is not None
            full_response.append(response)
    except (StopIteration, DoneException):
        pass
    assert len(full_response) > 0
