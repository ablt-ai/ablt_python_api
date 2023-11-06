# -*- coding: utf-8 -*-
"""
Filename: ablt_api_async.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 06.11.2023

Description:
This file contains an implementation of class for aBLT chat API.
"""

import asyncio
import json
import logging
import ssl
from datetime import datetime
from os import environ
from time import sleep
from typing import Optional, List, Dict

import aiohttp

from .schemas import StatisticsSchema, StatisticItemSchema, StatisticTotalSchema, BotSchema
from .utils.exceptions import DoneException
from .utils.logger_config import setup_logger


class ABLTApi:
    """aBLT Chat API master class"""

    def __init__(
            self,
            bearer_token: Optional[str] = None,
            base_api_url: str = "https://api.ablt.ai",
            logger: Optional[logging.Logger] = None,
            ssl_context: Optional[ssl.SSLContext] = None,
    ):
        """
        Initializes the object with the provided base API URL and bearer token.

        :param bearer_token: The bearer token for authentication.
        :type bearer_token: str
        :param base_api_url: The base API URL, default is 'https://api.ablt.ai'.
        :type base_api_url: str
        :param logger: default logger.
        :type logger: logger
        :param ssl_context: ssl context for aiohttp.
        :type ssl_context: ssl.SSLContext
        """
        self.__base_api_url = base_api_url
        if not bearer_token:
            if environ.get("ABLT_BEARER_TOKEN"):
                self.__bearer_token = environ["ABLT_BEARER_TOKEN"]
            else:
                raise TypeError("Bearer token is required!")
        else:
            self.__bearer_token = bearer_token
        self.__ssl_context = ssl_context
        if logger:
            self.__logger = logger
        else:
            self.__logger = setup_logger("api", "api.log")
            self.__logger.info("Logger for API now launched!")

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if loop.is_running():
            loop.create_task(self.update_api())
        else:
            loop.run_until_complete(self.update_api())

    def __get_url_and_headers(self, endpoint: str) -> tuple[str, dict]:
        """
        Constructs the URL and headers for an API request.

        :param endpoint: The endpoint for the API request.
        :type endpoint: str
        :return: The URL and headers for the API request.
        :rtype: tuple
        """
        url = f"{self.__base_api_url}/{endpoint}"
        headers = {"Authorization": f"Bearer {self.__bearer_token}"}
        return url, headers

    async def health_check(self) -> bool:
        """
        Performs a health check on the API.

        :return: True if the API status is 'ok', False otherwise.
        :rtype: bool
        """
        url, headers = self.__get_url_and_headers("health-check")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=self.__ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("status") == "ok":
                        self.__logger.info("ABLT chat API is working like a charm")
                        return True
                    self.__logger.error("Error: %s", data.get("status"))
                    try:
                        self.__logger.error("Error details:")
                        for error in data["detail"]:
                            self.__logger.error(
                                "  - %s (type: %s, location: %s)", error["msg"], error["type"], error["loc"]
                            )
                    except ValueError:
                        self.__logger.error("Error text: %s", response.text)
                        return False
                else:
                    self.__logger.error("Request error: %s", response.status)
                    try:
                        error_data = await response.json()
                        self.__logger.error("Error details:")
                        for original_error in error_data["detail"]:
                            self.__logger.error(
                                "  - %s (type: %s, location: %s)",
                                original_error["msg"],
                                original_error["type"],
                                original_error["loc"],
                            )
                    except ValueError:
                        self.__logger.error("Error text: %s", response.text)
                    return False

    async def get_bots(self) -> Optional[List[Dict[str, BotSchema]]]:
        """
        Retrieves all published bots.

        :return: A list of dictionaries containing bot information, or an empty list if an error occurs.
        :rtype: list of BotSchema
        """
        url, headers = self.__get_url_and_headers("v1/bots")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=self.__ssl_context) as response:
                if response.status == 200:
                    return await response.json()
                self.__logger.error("Request error: %s", response.status)
                try:
                    error_data = await response.json()
                    self.__logger.error("Error details: %s", error_data)
                except ValueError:
                    self.__logger.error("Error text: %s", await response.text())
                return None

    # pylint: disable=R0914,R0912,R0915
    async def chat(
            self,
            bot_uid: Optional[str] = None,
            bot_slug: Optional[str] = None,
            prompt: Optional[str] = None,
            messages=None,
            stream: Optional[bool] = False,
            user: Optional[str] = None,
            language: Optional[str] = None,
            assumptions: Optional[dict] = None,
            max_words: Optional[int] = None,
            use_search: Optional[bool] = False,
    ):
        """
        Sends a chat request to the API and returns the response.
        :param bot_uid: The id of the bot to chat with.
        :type bot_uid: str
        :param bot_slug: The slug of the bot to chat with.
        :type bot_slug: str
        :param prompt: The text prompt for the bot.
        :type prompt: str
        :param messages: A list of messages for the bot, each message is a dictionary with the following keys:
            - 'role' (str): the role of the message sender, either 'system', 'user', or 'assistant'
            - 'content' (str): the content of the message
        :type messages: list[dict]
        :param stream: A flag for streaming mode (default is False).
        :type stream: bool
        :param user: The user identifier.
        :type user: str
        :param language: The language of the chat, default is "English".
        :type language: str
        :param assumptions: The assumptions for the chat, default is None (TBD).
        :type assumptions: dict
        :param max_words: The maximum number of words in the response, if None, the default value is used.
        :type max_words: int
        :param use_search: A flag for using search mode (default is False).
        :type use_search: bool
        :return: The response message from the bot or None in case of an error.
        :rtype: yield
        :raises DoneException: If the bot is done with the conversation.

        Important: Only one of the parameters 'prompt' or 'messages' should be provided.
                   Only one of the parameters 'bot_uid' or 'bot_slug' should be provided.

        Errors:
        - If both 'prompt' and 'messages' parameters are missing or provided simultaneously, the function
          will print an error message and return None.
        - If the 'messages' parameter is provided, but its elements do not have the required keys or
          their values are not of the correct type, the function will print an error message and return None.

        Raises:
            DoneException: If the bot is done with the conversation.
        """
        if (not prompt and not messages) or (prompt and messages):
            self.__logger.error("Error: Only one param is required ('prompt' or 'messages')")
            return

        if (not bot_slug and not bot_uid) or (bot_slug and bot_uid):
            self.__logger.error("Error: Only one param is required ('bot_slug' or 'bot_uid')")
            return

        url, headers = self.__get_url_and_headers("v1/chat")
        payload = {
            "stream": stream,
            "use_search": use_search,
            **({"bot_slug": bot_slug} if bot_slug is not None else {}),
            **({"bot_uid": bot_uid} if bot_uid is not None else {}),
            **({"language": language} if language is not None else {}),
            **({"max_words": max_words} if max_words is not None else {}),
            **({"assumptions": assumptions} if assumptions is not None else {}),
            **({"prompt": prompt} if prompt is not None else {}),
            **({"messages": messages} if messages is not None else {}),
            **({"user": user} if user is not None else {}),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, ssl=self.__ssl_context) as response:
                if response.status == 200:
                    if stream:
                        try:
                            async for line in response.content.iter_any():
                                if line:
                                    line_data = line.decode("utf-8").splitlines()
                                    for data in line_data:
                                        if data.startswith("data:"):
                                            if "[DONE]" in data:
                                                raise DoneException
                                            data = data[5:].strip()
                                            try:
                                                message_data = json.loads(data)
                                            except json.JSONDecodeError:
                                                self.__logger.error("Seems json malformed %s", line)
                                                continue
                                            content = message_data.get("content")
                                            message = message_data.get("message")
                                            if content is not None:
                                                yield content
                                            elif message is not None:
                                                yield message
                        finally:
                            await response.release()
                    else:
                        response_json = await response.json()

                        if "message" in response_json:
                            message = response_json.get("message")
                        elif "content" in response_json:
                            message = response_json.get("content")
                        else:
                            self.__logger.error("Response malformed! Actual response is: %s", response_json)
                            return
                        yield message
                else:
                    self.__logger.error("Error: %s", response.status)
                    try:
                        error_data = await response.json()

                        self.__logger.error("Error details:")
                        if isinstance(error_data["detail"], str):
                            self.__logger.error("  - %s", error_data["detail"])
                        else:
                            for error in error_data["detail"]:
                                if error.get("msg") and error.get("type") and error.get("loc"):
                                    self.__logger.error(
                                        "  - %s (type: %s, location: %s)", error["msg"], error["type"], error["loc"]
                                    )
                                else:
                                    self.__logger.error("  - %s", error)
                    except ValueError:
                        error_text = await response.text()
                        self.__logger.error("Error text: %s", error_text)
                    return

    async def update_api(self) -> None:
        """
        Updates the API by calling the health_check function.

        :raises ConnectionError: If the health_check function fails 10 times in a row.

        Raises:
            ConnectionError: If the health_check function fails 10 times in a row.
        """
        retries = 0
        while retries <= 10:
            if not await self.health_check():
                retries += 1
                self.__logger.warning("WARNING: Seems something nasty happened with aBLT api, trying %s/10", retries)
                sleep(5)
            else:
                break
        if retries >= 10:
            raise ConnectionError("ERROR: Connection to aBLT API couldn't be established")

    async def set_base_api_url(self, new_base_api_url: str, instant_update: bool = False):
        """
        Sets a new base API URL.

        :param new_base_api_url: The new base API URL as a string.
        :type new_base_api_url: str
        :param instant_update: A boolean indicating whether to instantly update the API or not. Default is False.
        :type instant_update: bool
        """
        self.__base_api_url = new_base_api_url
        if instant_update:
            await self.update_api()

    async def set_bearer_token(self, new_bearer_token: str, instant_update: bool = False):
        """
        Sets a new bearer token.

        :param new_bearer_token: The new bearer token as a string.
        :type new_bearer_token: str
        :param instant_update: A boolean indicating whether to instantly update the API or not. Default is False.
        :type instant_update: bool
        """
        self.__bearer_token = new_bearer_token
        if instant_update:
            await self.update_api()

    async def update_api_info(self, new_bearer_token: str = None, new_base_api_url: str = None):
        """
        Updates the API information with new bearer token and/or new base API URL.

        :param new_bearer_token: The new bearer token as a string, if any. Default is None.
        :type new_bearer_token: str
        :param new_base_api_url: The new base API URL as a string, if any. Default is None.
        :type new_base_api_url: str
        - new_bearer_token (str): The new bearer token as a string, if any. Default is None.
        - new_base_api_url (str): The new base API URL as a string, if any. Default is None.
        """
        if new_bearer_token:
            await self.set_bearer_token(new_bearer_token)
        if new_base_api_url:
            await self.set_base_api_url(new_base_api_url)
        await self.update_api()

    def get_base_api_url(self) -> str:
        """
        Returns the current base API URL as a string.

        :return: The current base API URL as a string.
        :rtype: str
        """
        return self.__base_api_url

    def get_bearer_token(self) -> str:
        """
        Returns the current bearer token as a string.

        :return: The current bearer token as a string.
        :rtype: str
        """
        return self.__bearer_token

    def set_logger(self, new_logger: logging.Logger):
        """
        Sets logger for API

        Args:
        :param new_logger: new logger
        :type new_logger: logger
        """
        self.__logger = new_logger

    async def find_bot_by_uid(self, bot_uid: str) -> Optional[BotSchema]:
        """
        Searches for a bot by its id in the bot list.

        :param bot_uid: The id of the bot to search for.
        :type bot_uid: str
        :return: bot dict
        :rtype: BotSchema | None
        """
        for bot_info in await self.get_bots():
            if bot_info.get("uid") == bot_uid:
                return bot_info
        return None

    async def find_bot_by_slug(self, bot_slug: str) -> Optional[BotSchema]:
        """
        Searches for a bot by its slug in the bot list.

        :param bot_slug: The slug of the bot to search for.
        :type bot_slug: str
        :return: bot dict
        :rtype: BotSchema | None
        """
        for bot_info in await self.get_bots():
            if bot_info.get("slug") == bot_slug:
                return bot_info
        return None

    async def find_bot_by_name(self, bot_name: str) -> Optional[BotSchema]:
        """
        Searches for a bot by its name in the bot list.

        :param bot_name: The name of the bot to search for.
        :type bot_name: str
        :return: bot dict
        :rtype: BotSchema | None
        """
        for bot_info in await self.get_bots():
            if bot_info.get("name") == bot_name:
                return bot_info
        return None

    async def get_usage_statistics(
            self,
            user_id: str = "-1",
            start_date: str = datetime.now().strftime("%Y-%m-%d"),
            end_date: str = datetime.now().strftime("%Y-%m-%d"),
    ) -> Optional[StatisticsSchema]:
        """
        Retrieves usage statistics for the API.

        :param user_id: The id of the user to get statistics for.
        :type user_id: str
        :param start_date: The start date for the statistics in format YYYY-MM-DD.
        :type start_date: str
        :param end_date: The end date for the statistics in format YYYY-MM-DD.
        :type end_date: str
        :return: The response message from the bot or None in case of an error.
        :rtype: StatisticsSchema | None
        """
        url, headers = self.__get_url_and_headers("v1/user/usage-statistics")
        payload = {"user_id": user_id, "start_date": start_date, "end_date": end_date}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, ssl=self.__ssl_context) as response:
                if response.status == 200:
                    return await response.json()
                self.__logger.error("Request error: %s", response.status)
                try:
                    error_data = await response.json()
                    self.__logger.error("Error details: %s", error_data)
                except ValueError:
                    self.__logger.error("Error text: %s", await response.text())
                return None

    async def get_statistics_for_a_day(self, user_id: str, date: str) -> Optional[StatisticItemSchema]:
        """
        Retrieves usage statistics for the API.

        :param user_id: The id of the user to get statistics for.
        :type user_id: str
        :param date: day for which statistics are needed. It should be in format YYYY-MM-DD.
        :type date: str
        :return: dict with statistics for a day.
        :rtype: StatisticItemSchema | None.
        """
        items = (await self.get_usage_statistics(user_id=user_id, start_date=date, end_date=date)).get("items")
        for usage_info in items:
            if usage_info.get("date") == date:
                return usage_info
        return None

    async def get_statistics_total(self, user_id: str, start_date: str, end_date: str) -> StatisticTotalSchema:
        """
        Retrieves usage statistics for the API.

        :param user_id: The id of the user to get statistics for.
        :type user_id: int
        :param start_date: start date for statistics.
        :type start_date: str
        :param end_date: end date for statistics.
        :type end_date: str
        :return: dict with total statistics.
        :rtype: StatisticTotalSchema.
        """
        return (await self.get_usage_statistics(user_id=user_id, start_date=start_date, end_date=end_date)).get("total")
