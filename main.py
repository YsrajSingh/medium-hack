"""This module provides various utility classes and functions to fetch data (in list) of followers of target user."""
from secret.helper import JsonObjectReader, JsonFileWriter, ApiHandler
import secret.constants as constants


class GetUsersList:
    """
    A class for fetching and storing user data based on username and user type.

    Attributes:
        user_name (str): The username for which user data is to be fetched.
        is_optional (bool): Indicates whether the data is optional or not.
        all_user_data (list): A list to store user data.
        json_file (JsonObjectReader): An instance of JsonObjectReader for reading JSON data.
        json_write_file (JsonFileWriter): An instance of JsonFileWriter for writing JSON data.
        response (str): A response message indicating the status of data fetching.
    """

    def __init__(self, user_name: str, optional: bool):
        """
        Initialize a GetUsersList instance.

        Args:
            user_name (str): The username for which user data is to be fetched.
            optional (bool): Indicates whether the data is optional or not.
        """
        self.user_name = user_name
        self.is_optional = optional
        self.all_user_data = []
        self.json_file = JsonObjectReader()
        self.json_write_file = JsonFileWriter(
            constants.PATH_USER_FILE if self.is_optional else constants.PATH_TARGET_FILE
        )
        self.response = self.fetch_data()

    def __str__(self) -> str:
        """
        Return a string representation of the GetUsersList instance.

        Returns:
            str: A string containing the response message.
        """
        return str(self.response)

    def optional(self, data: dict) -> str:
        """
        Get the value of the 'ID' field from the data dictionary if it exists.

        Args:
            data (dict): The data dictionary.

        Returns:
            str: The value of 'ID' if it exists, or an empty string.
        """
        if self.is_optional:
            if isinstance(data, dict):
                return data.get(constants.ID)
            elif isinstance(data, list) and data:
                return data[0].get(constants.ID)

    def setup_api_request(self):
        """Set up the API request configuration based on user type (optional or not)."""
        self.json_data = self.json_file.fetch_json_by_name(
            constants.FETCH_FOLLOWING_LIST
            if self.is_optional
            else constants.FETCH_FOLLOWERS_LIST
        )
        self.json_data[constants.BODY][constants.VARIABLES][
            constants.USER_NAME
        ] = self.user_name
        self.json_data[constants.BODY][constants.VARIABLES][
            constants.ID
        ] = self.json_data[constants.BODY][constants.VARIABLES][constants.PAGING][
            constants.FROM
        ] = None
        self.api_handler = ApiHandler(
            self.json_data[constants.URL], self.json_data[constants.HEADER]
        )

    def initial_data(self) -> str:
        """
        Fetch initial user data and return the next 'from_user_id' (next user id or id's).

        Returns:
            str: The next 'from_user_id' (next user id or id's) or an empty string.
        """
        self.setup_api_request()
        response_status, response_data = self.api_handler.json_call_handler(
            self.json_data[constants.BODY]
        )
        if response_status == 200 and response_data:
            initial_users = (
                response_data[constants.DATA][constants.USER_RESULT][
                    constants.FOLLOWING_USERS_CONNECTIONS
                ][constants.USERS]
                if self.is_optional
                else response_data[constants.DATA][constants.USER_RESULT][
                    constants.FOLLOWERS_USERS_CONNECTIONS
                ][constants.USERS][0]
            )

            if self.is_optional:
                for user in initial_users:
                    self.all_user_data.append(user[constants.ID])
            else:
                self.all_user_data.append(initial_users)

            return (
                response_data[constants.DATA][constants.USER_RESULT][
                    constants.FOLLOWING_USERS_CONNECTIONS
                ][constants.PAGING_INFO][constants.NEXT][constants.FROM]
                if self.is_optional
                else initial_users[constants.ID]
            )

    def fetch_data(self) -> str:
        """
        Fetch user data and store it.

        Returns:
            str: A message indicating the status of data fetching.
        """
        from_user_id = self.initial_data()

        while from_user_id:
            print(constants.LOADING)
            self.json_data[constants.BODY][constants.VARIABLES][constants.PAGING][
                constants.FROM
            ] = from_user_id
            response_status, response_data = self.api_handler.json_call_handler(
                self.json_data[constants.BODY]
            )

            if response_data is None:
                print(constants.ERROR_NONE_API_RESPONSE)
                break

            if response_status == 200 and response_data:
                new_result = response_data
                user_data = (
                    new_result[constants.DATA][constants.USER_RESULT][
                        constants.FOLLOWING_USERS_CONNECTIONS
                    ][constants.USERS]
                    if self.is_optional
                    else new_result[constants.DATA][constants.USER_RESULT][
                        constants.FOLLOWERS_USERS_CONNECTIONS
                    ][constants.USERS]
                )
                if self.is_optional:
                    user_ids = [
                        user.get(constants.ID)
                        for user in user_data
                        if user.get(constants.ID)
                    ]
                    self.all_user_data.extend(user_ids)
                    paging_info = response_data[constants.DATA][constants.USER_RESULT][
                        constants.FOLLOWING_USERS_CONNECTIONS
                    ][constants.PAGING_INFO]
                    next_data = paging_info.get(constants.NEXT)
                    if next_data:
                        from_user_id = next_data.get(constants.FROM)
                    else:
                        from_user_id = None
                else:
                    self.all_user_data.extend(user_data)
                    from_user_id = user_data[-1][constants.ID] if user_data else None

        if self.all_user_data:
            self.json_write_file.write_file(self.all_user_data)
        return constants.DATA_FETCHING_COMPLETED
