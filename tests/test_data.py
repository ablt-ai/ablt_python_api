# -*- coding: utf-8 -*-
"""
Filename: test_data.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

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
