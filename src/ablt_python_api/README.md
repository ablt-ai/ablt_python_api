# aBLT Python API wrapper

[![PyPI version](https://badge.fury.io/py/ablt-python-api.svg)](https://badge.fury.io/py/ablt-python-api) [![Linters](https://github.com/ablt-ai/ablt_python_api/actions/workflows/master_linters.yml/badge.svg?branch=master)](https://github.com/ablt-ai/ablt_python_api/actions/workflows/master_linters.yml) [![Tests](https://github.com/ablt-ai/ablt_python_api/actions/workflows/master_tests.yml/badge.svg?branch=master)](https://github.com/ablt-ai/ablt_python_api/actions/workflows/master_tests.yml)

# About

This is Python aBLT API wrapper. It is used to communicate with aBLT API. You may use it to create your own aBLT client using asynchronous or synchronous Python. You can find more information about aBLT API [here](https://docs.ablt.ai/api_docs/overview).

At first, you need obtain aBLT API Token. You can do it [here](https://ablt.ai/) by get in touch and contact with support for paid plans. Next, you may use any existing ready-made bots or templates or create your own bot via UI interface.

# Installation

API wrapper is available on PyPI. You can install it with pip (recommended to use Python 3.9+):

```bash
pip install ablt-python-api
```

# Usage

Then you can import it and use it:

```python
# for asynchronous API wrapper use ABLTApi_async
from ablt_python_api import ABLTApi  # this is synchronous API wrapper


# Init with explicit token
api = ABLTApi(bearer_token=YOUR_ABLT_API_TOKEN)

# Init with environment variable, use ABLT_BEARER_TOKEN
api = ABLTApi()
```

For some reason you may want to use your own logger, then you can initialize API wrapper with logger:

```python
# logger it's pre-configured instance of logging.logger
api = ABLTApi(logger=your_logger)
```

# API methods

## Bots

### List of bots

You may get list of bots:

```python
# will return list of bots, see schema docs: https://docs.ablt.ai/api_docs/bots/get#Response-body
bots = api.api.get_bots()  
```

Or you may use actual schema:

```python
from ablt_python_api.schemas import BotsSchema


# Use await for asynchronous API wrapper
bots = [BotsSchema.model_validate(bot_dict) for bot_dict in api.get_bots()]  
```

### Single bot

You may get bot by UID:

```python
bot = api.find_bot_by_uid(bot_uid='F0b98A09-c5ed-1197-90F3-BBfF1DBb28ee')
```

Alternatively, you may get bot by slug:

```python
bot = api.find_bot_by_slug(bot_slug='omni')
```

Or by name (but it's not recommended, because name may be not unique):

```python
bot = api.find_bot_by_name(bot_name='Miles Hiker')
```

In case if no bot found, then `None` will be returned.

### Chat

To chat with bot you may use `chat' method:

```python
# Specify bot UID, will return generator with bot responses.
response = api.chat(bot_uid=BOT_UID, prompt='Hello, bot!')
# Or specify bot slug, return generator with bot responses.
response = api.chat(bot_slug=BOT_SLUG, prompt='Hello, bot!')
# To get response as string, you may use loop or extract just first response from generator
str_response = response.__next__()
# Or use __anext__ for async mode
```

Most probably, you will use `messages` list instead of `prompt` to save context. In this case, you may call method like
following:

```python
messages = [
    {"content": "I like to eat pizza", "role": "user"},
    {"content": "Hello, I like pizza too!", "role": "assistant"},
    {"content": "What do I like to eat?", "role": "user"},
]
# Will return generator with bot response
response = api.chat(bot_uid=BOT_UID, messages=messages)  
```

You need ensure, that your prompt is last message in `messages` list. 

### More options

Additionally, you may extend \ override system context with passing `system` instruction to bot:

```python
# Use with caution, it may conflict or replace all settings stored in UI 
# and may lead to unexpected results
messages = [
               {"content": "You are a bibliophile bot, you know everything about literature", "role": "system"},
               {"content": "Who is author of 'The Sirens of Titan'?", "role": "user"},
           ],
```

You may call `chat` method with params to override system settings, if you want:

```python
response = api.chat(bot_uid=BOT_UID,
                    prompt='Hello, bot!',
                    language='Arabic',  # may be: "Arabic", "French", "English", "Spanish", "Russian"
                    max_words=100,  # any integer, values less than 100 and greater than 2000 not recommended
                    user_id=42,  # unique user ID, used to split up usage statistics per user
                    use_search=False)  # use search mode, if True, then bot will try to find answer in internet
```

_Notes_:
In general, you may to try to use unusual values for:
* `language`, like "Serbian", but it's not guaranteed that it will work as you expected. 
* `max_words` - you may try to use values less than 100 words to save tokens, but you may be experienced with cut-offs. For values greater than 2000 words you may be experienced with timeouts or errors for regular, not 32k or 128k models.
* `user_id` - you may use any integer value, but it's recommended to use your own unique user ID, because it's used to split up usage statistics per user.
* `use_search` - it's special feature for premium plans, you may try to manage it from API, and not from UI, but it's highly not recommended to use with smaller `max_words` values, so, while using search, please use values at least 100 or more for `max words`.

### Streaming mode

By default, bots are working in streaming mode (as in UI), so, you may use `chat` method to chat with bot in streaming mode, but you may to switch it off by:

```python
response = api.chat(bot_uid=BOT_UID, prompt='Hello, bot!', stream=False)
```

In case if you prefer to use streaming mode, you need to get response from generator:

```python
import sys

from ablt_python_api import DoneException


try:
    for response in api.chat(bot_uid=BOT_UID, prompt='Hello, bot!', stream=True):
        # I use direct stdout output to make output be printed on-the-fly
        sys.stdout.write(response)  
        # To get typewriter effect I forcefully flush output each time
        sys.stdout.flush()  
except DoneException:
    pass  # DoneException is raised when bot finished conversation
```

## Statistics

Statistics may be used to obtain data for words and tokens usage for period of time. 

### Full statistics

```python
# Will return statistics for current date for default user = -1
statistics_for_today = api.get_usage_statistics()  
# Will return statistics for date range
statistics_for_range = api.get_usage_statistics(start_date='2022-02-24', 
                                                end_date='2023-11-17')
# Will return statistics for user with ID 42
statistics_for_user = api.get_usage_statistics(user_id=42)  
```

You may use schema to validate statistics:

```python
from ablt_python_api.schemas import StatisticsSchema


statistics = StatisticsSchema.model_validate(api.get_usage_statistics())
```

### Statistic for a day

```python
# Will return statistics for current date for user = -1
statistics_for_today = api.get_usage_statistics_for_day()
# Will return statistics for specified date
statistics_for_specific_day = api.get_usage_statistics_for_day(date='2022-02-24')
# Will return statistics for user with ID 42
statistics_for_user = api.get_usage_statistics_for_day(user_id=42)  
```

With schema:

```python
from ablt_python_api.schemas import StatisticItemSchema


statistics = StatisticItemSchema.model_validate(api.get_usage_statistics_for_day())
```

### Total statistics

```python
# Will return statistics for current date for user = -1
statistics_for_today = api.get_total_usage_statistics()
# Well return statistics for specified date
statistics_for_specific_day = api.get_total_usage_statistics(date='2022-02-24')
# Will return statistics for user with ID 42
statistics_for_user = api.get_total_usage_statistics(user_id=42)  
```

With schema:

```python
from ablt_python_api.schemas import StatisticTotalSchema


statistics = StatisticTotalSchema.model_validate(api.get_usage_statistics_for_day())
```

# Troubleshooting:

You can always [contact support](mailto:contact@aBLT.ai) or contact us in [Discord channel](https://discord.com/channels/1097998898506760392/1104055996302766120).

## SSL errors

In some cases, you may be experienced with SSL errors, then you may disable certificate verification:

```python
import ssl


sslcontext = ssl.create_default_context()
sslcontext.check_hostname = False
sslcontext.verify_mode = ssl.CERT_NONE

ABLTApi_async(ssl_context=sslcontext)  # for async
ABLTApl(ssl_verify=False)  # for sync
```

## Rate limit errors

Never try to flood API with requests, because you may be experienced with rate limit errors. In this case, you need to wait for some time and retry your request. Especially, never try to flood API with simultaneous requests for more users than allowed in your plan.

## Timeout errors

In some cases, you may be experienced with timeout errors, then you may decrease `max_words` value or use `stream = True` to get response on-the-fly.

## Other errors

In vary rare cases, you may be experienced with other errors, like rebooting of API itself. To check-up API health, you may use `health_check` method:

```python
# will return True if API is healthy, otherwise False
api.health_check()  
```

# Best practices

Always check-up and follow [Guides](https://docs.ablt.ai/guides/overview), [References](https://docs.ablt.ai/reference/overview) and [Examples](https://docs.ablt.ai/examples) from ABLT documentation.
