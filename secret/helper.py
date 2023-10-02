import json
import os
import requests


class JsonFileWriter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_data = []
        self.create_file()

    def write_file(self, data_list):
        self.file_data = data_list
        self.create_file()

    def create_file(self):
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w") as file:
                json.dump(self.file_data, file)
        except IOError as e:
            raise IOError(f"Error writing to file '{self.file_path}': {e}")


class JsonFileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_data = self.read_file()

    def __str__(self):
        return str(self.file_data)

    def read_file(self):
        try:
            with open(self.file_path) as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{self.file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file '{self.file_path}': {e}")


class JsonObjectReader:
    def __init__(self, file_path="secret/json/config.json"):
        self.file_path = file_path
        self.read_file()

    def read_file(self):
        try:
            with open(self.file_path) as f:
                self.file_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file '{self.file_path}' not found.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON file '{self.file_path}': {e}")

    def fetch_json_by_name(self, key):
        try:
            value = self.file_data[key]
            return value
        except KeyError:
            raise KeyError(f"Key '{key}' not found in JSON data.")


class ApiHandler:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers or {}

    def _make_request(self, body, data_format):
        try:
            response = requests.post(self.url, headers=self.headers, **data_format)
            return response.status_code, response.json()
        except requests.exceptions.RequestException as e:
            return f"Request failed with error: {e}"

    def json_call_handler(self, body):
        data_format = {"json": body}
        return self._make_request(body, data_format)

    def text_call_handler(self, body):
        data_format = {"data": body}
        return self._make_request(body, data_format)
