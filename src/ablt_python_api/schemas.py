# -*- coding: utf-8 -*-
"""
Filename: schemas.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 06.11.2023
Last Modified: 06.11.2023

Description:
This file contains schemas for aBLT.ai API.
"""

from datetime import date
from typing import List
from typing import Optional

from pydantic import BaseModel


class StatisticItemSchema(BaseModel):
    """This class represents a single item in statistics."""

    original_tokens: int
    enchancement_tokens: int
    response_tokens: int
    total_tokens: int
    original_words: int
    enchancement_words: int
    response_words: int
    total_words: int
    date: date


class StatisticTotalSchema(BaseModel):
    """This class represents total statistics."""

    original_tokens: int
    enchancement_tokens: int
    response_tokens: int
    total_tokens: int
    original_words: int
    enchancement_words: int
    response_words: int
    total_words: int


class StatisticsSchema(BaseModel):
    """This class represents statistics."""

    total: StatisticTotalSchema
    items: List[StatisticItemSchema]


class StatisticsRequestSchema(BaseModel):
    """This class represents statistics request."""

    user_uid: str
    start_date: date
    end_date: date


class BotSchema(BaseModel):
    """This class represents a bot."""

    uid: str
    slug: str
    model: str
    name: str
    description: str
    welcome_message: str
    avatar_url: Optional[str]
