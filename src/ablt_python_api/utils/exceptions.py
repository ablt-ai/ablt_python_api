"""
Filename: exceptions.py
Author: Iliya Vereshchagin
Copyright (c) 2023 aBLT.ai. All rights reserved.

Created: 14.06.2023
Last Modified: 19.06.2023

Description:
This file contains any exception classes.
"""


class DoneException(Exception):
    """This class is dummy placeholder to raise exception to break endless stream responses (endless loop)"""


class CustomError(Exception):
    """This class is placeholder to raise exception for servers or standalone logging"""

    def __init__(self, message: str, status_code: int, data: str = ""):
        """
        Init CustomError class

        :param message: error message
        :type message: str
        :param status_code: status code
        :type status_code: int
        :param data: data to return
        :type data: str
        """
        super().__init__(message)
        self.status_code = status_code
        self.data = data
