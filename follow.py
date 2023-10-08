"""This module provides classes and function to handle (Medium's) Follow API."""
from secret.helper import JsonObjectReader, JsonFileReader, ApiHandler
from secret import constants


class FollowUserList:
    """
    A class for following a list of users.

    Attributes:
        header_token (str): The authentication token for making API requests.
        json_object (JsonObjectReader): An instance of JsonObjectReader for reading JSON data.
        target_file (JsonFileReader): An instance of JsonFileReader for reading the target user file.
        my_followers_file (JsonFileReader): An instance of JsonFileReader for reading the user's followers file.
        json_data (dict): JSON data containing configuration.
        api_handler (ApiHandler): An instance of ApiHandler for making API requests.
        followed_count (int): The count of users followed.
    """

    def __init__(self, header_token: str):
        """
        Initialize a FollowUserList instance.

        Args:
            header_token (str): The authentication token for making API requests.
        """
        self.json_object = JsonObjectReader()
        self.target_file = JsonFileReader(constants.PATH_TARGET_FILE)
        self.my_followers_file = JsonFileReader(constants.PATH_USER_FILE)
        self.json_data = self.json_object.fetch_json_by_name(constants.FOLLOW_USERS)
        self.json_data[constants.HEADER][constants.COOKIE] = header_token
        self.api_handler = ApiHandler(
            self.json_data[constants.URL], self.json_data[constants.HEADER]
        )
        self.followed_count = 0
        self.follow_users()

    def follow_users(self):
        """Follow users based on the configuration and target user list (based on target user Id)."""
        for user in self.target_file.file_data:
            if self.followed_count >= 150:
                print(constants.ERROR_LIMIT_EXCEEDED)
                break
            user_id = user.get(constants.ID)
            if user_id not in self.my_followers_file.file_data:
                self.json_data[constants.BODY][constants.VARIABLES][
                    constants.TARGET_USER_ID
                ] = user_id
                response_status, response_data = self.api_handler.json_call_handler(
                    self.json_data[constants.BODY]
                )
                if response_status == 200 and response_data:
                    self.followed_count += 1
                    print(f"{constants.USER_FOLLOWED_WITH_ID}: {user_id}")
                else:
                    print(
                        f"{constants.ERROR_FAILED_WITH_STATUS_CODE} : {response_status} for {user_id}"
                    )
            else:
                print(f"{constants.ALREADY_FOLLOWED_YOU}, {constants.ID}: {user_id}")

    def __str__(self) -> str:
        """
        Return the number of users followed in form of string.

        Returns:
            str: A string containing the count of users followed.
        """
        return f"{constants.COUNT_FOLLOWED_USERS}: {self.followed_count}"
