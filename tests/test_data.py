# -*- coding: utf-8 -*-
"""
Filename: test_data.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 06.11.2023

Description:
This file contains data for tests.
"""
import ssl
from random import randint

sslcontext = ssl.create_default_context()
sslcontext.check_hostname = False
sslcontext.verify_mode = ssl.CERT_NONE

unique_models = (
    "claude-2-aws-bedrock",
    "claude-aws-bedrock",
    "claude-instant-aws-bedrock",
    "claude-llama-2-34-b-anyscale",
    "command-cohere",
    "command-nightly-cohere",
    "command-light-nightly-cohere",
    "gpt-3-5-turbo-0613-open-ai",
    "gpt-3-5-turbo-open-ai",
    "gpt-4-0613-open-ai",
    "gpt-4-open-ai",
    "gpt-4-32-k-azure",
    "gpt-4-azure",
    "llama2-13-b-anyscale",
    "llama2-70-b-anyscale",
    "llama2-7-b-anyscale",
    "llama-v2-13b-chat-fireworks-ai",
    "llama-v2-13b-code-instruct-fireworks-ai",
    "llama-v2-34b-code-instruct-fireworks-ai",
    "llama-v2-70b-chat-fireworks-ai",
    "llama-v2-7b-chat-fireworks-ai",
    "mistral-7b-instruct-4k-fireworks-ai",
    "palm-2",
    "Palm-2-vertex-ai",
)
sample_questions = (
    "What is the capital of France?",
    "Who is the first president of the United States?",
    "Whose rule the galaxy in Warhammer 40k?",
    "What is the answer to life, the universe and everything?",
    "Name the mexican sweet bread?",
    "Tell me formula of gunpowder?",
    "What is the first game of Westwood Studios?",
    "Is Putin war criminal?",
    "What is the most famous horror movie?",
    "Where can I find the best pizza in New York?",
)
KEY_LENGTH = randint(8, 32)
MIN_WORDS = 3
SOME_USER_ID_RANGE = 65536
DATE_TEST_PERIOD = 365

ensured_bots = (
    {
        "uid": "9c24d711-e599-421c-a5fa-d15e113f14f6",
        "slug": "omni",
        "model": "gpt-4",
        "name": "Omni",
        "description": "An omniscient bot with knowledge of everything",
        "welcome_message": "Hi, I'm Omni. \n\nHow can I help you today?",
        "avatar_url": "https://strapi-ablt.s3.amazonaws.com/thumbnail_omni_bdf1a23d4e.jpg",
    },
    {
        "uid": "74b9d85e-10Ac-3e6B-bfCF-dc8A77E2FDC3",
        "slug": "eco",
        "model": "gpt-4",
        "name": "Eco",
        "description": "Your guide to recycling, upcycling, and the environment",
        "welcome_message": "Hey dude! I'm Eco, your gnarly guide to all things green and clean.\n\nWhat's up?",
        "avatar_url": "https://strapi-ablt.s3.amazonaws.com/thumbnail_recycle_a42d696442.jpg",
    },
    {
        "uid": "bD2EFCaD-1030-2AaE-9657-6DAB6f30e5be",
        "slug": "character",
        "model": "gpt-4",
        "name": "Character Template",
        "description": "Create AI characters for yourself or business",
        "welcome_message": "Hello. How can I help you today?",
        "avatar_url": "https://strapi-ablt.s3.amazonaws.com/thumbnail_666201_3b63097729.jpg",
    },
)


