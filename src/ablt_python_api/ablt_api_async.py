# -*- coding: utf-8 -*-
"""
Filename: __init__.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 03.11.2023
Last Modified: 03.11.2023

Description:
This file contains an implementation of class for aBLT chat API.
"""

import asyncio
import json
import logging
from time import sleep

import aiohttp

from .utils.exceptions import DoneException
from .utils.logger_config import setup_logger


class ABLTApi:
    """aBLT Chat API master class"""

    def __init__(
        self,
        bearer_token: str,
        base_api_url: str = "https://api.ablt.ai",
        logger: logging.Logger = None,
        ssl_context=None,
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

    def __get_url_and_headers(self, endpoint: str):
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

    async def health_check(self):
        """
        Performs a health check on the API.

        Args:
        - None

        Returns:
        - bool: True if the API status is 'ok', False otherwise
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
                        for error in error_data["detail"]:
                            self.__logger.error(
                                "  - %s (type: %s, location: %s)", error["msg"], error["type"], error["loc"]
                            )
                    except ValueError:
                        self.__logger.error("Error text: %s", response.text)
                    return False

    async def get_bots(self):
        """
        Retrieves all published bots.

        Args:
        - None

        Returns:
        - list: A list of dictionaries containing bot information, or an empty list if an error occurs
        """
        url, headers = self.__get_url_and_headers("v1/bots")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
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
        bot_uid=None,
        bot_slug=None,
        prompt=None,
        messages=None,
        stream=False,
        user=None,
        language=None,
        assumptions=None,
        max_words=None,
        use_search=False,
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

        Important: Only one of the parameters 'prompt' or 'messages' should be provided.
                   Only one of the parameters 'bot_uid' or 'bot_slug' should be provided.


        Errors:
        - If both 'prompt' and 'messages' parameters are missing or provided simultaneously, the function
          will print an error message and return None.
        - If the 'messages' parameter is provided, but its elements do not have the required keys or
          their values are not of the correct type, the function will print an error message and return None.
        """
        if (not prompt and not messages) or (prompt and messages):
            self.__logger.error("Error: Only one param is required ('prompt' or 'messages')")
            return

        if (not bot_slug and not bot_uid) or (bot_slug and bot_uid):
            self.__logger.error("Error: Only one param is required ('bot_slug' or 'bot_uid')")
            return

        url, headers = self.__get_url_and_headers("v1/chat")
        data = {
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
            async with session.post(url, headers=headers, json=data, ssl=self.__ssl_context) as response:
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
                            message = response_json["message"]
                        elif "content" in response_json:
                            message = response_json["content"]
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

    async def update_api(self):
        """
        Updates the API by calling the health_check function.

        Args:
        - None

        Returns:
        - None
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

    async def set_base_api_url(self, new_base_api_url, instant_update=False):
        """
        Sets a new base API URL.

        Args:
        - new_base_api_url (str): The new base API URL as a string.
        - instant_update (bool): A boolean indicating whether to instantly update the API or not. Default is False.

        Returns:
        - None
        """
        self.__base_api_url = new_base_api_url
        if instant_update:
            await self.update_api()

    async def set_bearer_token(self, new_bearer_token, instant_update=False):
        """
        Sets a new bearer token.

        - new_bearer_token (str): The new bearer token as a string.
        - instant_update (bool): A boolean indicating whether to instantly update the API or not. Default is False.

        Args:
        - None

        Returns:
        - None
        """
        self.__bearer_token = new_bearer_token
        if instant_update:
            await self.update_api()

    async def update_api_info(self, new_bearer_token=None, new_base_api_url=None):
        """
        Updates the API information with new bearer token and/or new base API URL.

        - new_bearer_token (str): The new bearer token as a string, if any. Default is None.
        - new_base_api_url (bool): The new base API URL as a string, if any. Default is None.

        Args:
        - None

        Returns:
        - None
        """
        if new_bearer_token:
            await self.set_bearer_token(new_bearer_token)
        if new_base_api_url:
            await self.set_base_api_url(new_base_api_url)
        await self.update_api()

    def get_base_api_url(self):
        """
        Returns the current base API URL as a string.

        Args:
        - None

        Returns:
        - str: current base API URL
        """
        return self.__base_api_url

    def get_bearer_token(self):
        """
        Returns the current bearer token as a string.

        Args:
        - None

        Returns:
        - str: current bearer token
        """
        return self.__bearer_token

    def set_logger(self, new_logger):
        """
        Sets logger for API

        Args:
        - logger (logger): default logger

        Returns:
        - None
        """
        self.__logger = new_logger

    async def find_bot_by_uid(self, bot_uid):
        """
        Searches for a bot by its id in the bot list.

        Args:
        - bot_uid (str): The id of the bot to search for.

        Returns:
        - str: bot dict
        """

        for bot_info in await self.get_bots():
            if bot_info.get("uid") == bot_uid:
                return bot_info
        return None

    async def find_bot_by_slug(self, bot_slug):
        """
        Searches for a bot by its slug in the bot list.

        Args:
        - bot_slug (str): The slug of the bot to search for.

        Returns:
        - str: bot dict
        """

        for bot_info in await self.get_bots():
            if bot_info.get("slug") == bot_slug:
                return bot_info
        return None

    async def find_bot_by_name(self, bot_name):
        """
        Searches for a bot by its name in the bot list.

        Args:
        - bot_name (str): The name of the bot to search for.

        Returns:
        - str: bot dict
        """

        for bot_info in await self.get_bots():
            if bot_info.get("name") == bot_name:
                return bot_info
        return None

    async def get_usage_statistics(self):
        """
        Retrieves usage statistics for the API.

        :return: The response message from the bot or None in case of an error.
        :rtype: dict.
        """

        url, headers = self.__get_url_and_headers("/v1/user/usage-statistics")
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, ssl=self.__ssl_context) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                self.__logger.error("Request error: %s", response.status)
                try:
                    error_data = await response.json()
                    self.__logger.error("Error details: %s", error_data)
                except ValueError:
                    self.__logger.error("Error text: %s", await response.text())
                return None

    async def get_statistics_for_a_day(self, day: str):
        """
        Retrieves usage statistics for the API.

        :param day: day for which statistics are needed. It should be in format YYYY-MM-DD.
        :return: dict with statistics for a day.
        :rtype: dict.
        """
        items = self.get_usage_statistics().get("items")
        for usage_info in await items:
            if usage_info.get("date") == day:
                return usage_info
        return None
