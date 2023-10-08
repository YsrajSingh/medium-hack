"""This module provides various utility classes and functions for working with JSON data, file I/O, and API handling."""
import json
import os
import requests
from typing import Dict, Any, Tuple, Optional

import secret.constants as constants


class JsonFileWriter:
    """
    A class for writing data to a JSON file.

    Attributes:
        file_path (str): The path to the JSON file.
        file_data (list): The data to be written to the file.
    """

    def __init__(self, file_path: str):
        """
        Initialize a JsonFileWriter instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        self.file_data = []
        self.create_file()

    def write_file(self, data_list: list):
        """
        Write the given data list to the JSON file.

        Args:
            data_list (list): The data to be written to the file.
        """
        self.file_data = data_list
        self.create_file()

    def create_file(self):
        """Create the JSON file and writes data to it."""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as file:
                json.dump(self.file_data, file)
        except IOError as e:
            raise IOError(f"{constants.ERROR_IN_WRITING_FILE} '{self.file_path}': {e}")


class JsonFileReader:
    """
    A class for reading data from a JSON file.

    Attributes:
        file_path (str): The path to the JSON file.
    """

    def __init__(self, file_path: str):
        """
        Initialize a JsonFileReader instance.

        Args:
            file_path (str): The path to the JSON file.
        """
        self.file_path = file_path
        self.file_data = self.read_file()

    def __str__(self) -> str:
        """Return file data in string format."""
        return str(self.file_data)

    def read_file(self) -> Optional[list]:
        """
        Read data from the JSON file.

        Returns:
            list: The data read from the file.
        """
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            return None
            # raise FileNotFoundError(f"JSON file '{self.file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"{constants.ERROR_IN_DECODING_FILE} '{self.file_path}': {e}"
            )


class JsonObjectReader:
    """
    A class for reading data from a JSON object.

    Attributes:
        file_path (str): The path to the JSON file (default is constants.PATH_DEFAULT_JSON_FILE_READER).
        file_data (dict): The data read from the JSON file.
    """

    def __init__(self, file_path: str = constants.PATH_DEFAULT_JSON_FILE_READER):
        """
        Initialize a JsonObjectReader instance.

        Args:
            file_path (str, optional): The path to the JSON file. Defaults to constants.PATH_DEFAULT_JSON_FILE_READER.
        """
        self.file_path = file_path
        self.read_file()

    def read_file(self):
        """
        Read data from the JSON file and stores it in the file_data attribute.

        Returns:
            dict: The data read from the JSON file.
        """
        try:
            with open(self.file_path) as f:
                self.file_data = json.load(f)
        except FileNotFoundError:
            return None
            # raise FileNotFoundError(f"JSON file '{self.file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(
                f"{constants.ERROR_IN_DECODING_FILE} '{self.file_path}': {e}"
            )

    def fetch_json_by_name(self, key: str) -> Any:
        """
        Fetch a JSON value by the given key from the file_data attribute.

        Args:
            key (str): The key for the JSON value.

        Returns:
            Any: The JSON value associated with the key.
        Raises:
            KeyError: If the key is not found in the JSON data.
        """
        try:
            value = self.file_data[key]
            return value
        except KeyError:
            raise KeyError(f"{constants.ERROR_KEY_NOT_FOUND} : {key}.")


class ApiHandler:
    """
    A class for handling API requests.

    Attributes:
        url (str): The URL of the API.
        headers (dict): The headers to be included in API requests (default is an empty dictionary).
    """

    def __init__(self, url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize an ApiHandler instance.

        Args:
            url (str): The URL of the API.
            headers (dict, optional): The headers to be included in API requests. Defaults to None.
        """
        self.url = url
        self.headers = headers or {}

    def _make_request(
        self, body: Dict[str, Any], data_format: Dict[str, Any]
    ) -> Tuple[int, Any]:
        """
        Make an API request with the specified body and data format.

        Args:
            body (dict): The data to be sent in the API request body.
            data_format (dict): The data format for the request (e.g., {'json': body}).

        Returns:
            tuple: A tuple containing the HTTP status code and the JSON response data.

        Raises:
            str: If there is an error in making the API request.
        """
        try:
            response = requests.post(self.url, headers=self.headers, **data_format)
            return response.status_code, response.json()
        except requests.exceptions.RequestException as e:
            return f"{constants.ERROR_FAILED_WITH_ERROR}: {e}"

    def json_call_handler(self, body: Dict[str, Any]) -> Tuple[str, Any]:
        """
        Make an API request with JSON data.

        Args:
            body (dict): The JSON data to be sent in the API request body.

        Returns:
            tuple: A tuple containing the HTTP status code and the JSON response data.
        """
        data_format = {constants.JSON: body}
        return self._make_request(body, data_format)

    def text_call_handler(self, body: Dict[str, Any]) -> Tuple[int, Any]:
        """
        Make an API request with text data.

        Args:
            body (str): The text data to be sent in the API request body.

        Returns:
            tuple: A tuple containing the HTTP status code and the JSON response data.
        """
        data_format = {constants.DATA: body}
        return self._make_request(body, data_format)
