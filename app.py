"""
The Medium Hack Application.

This script is a part of The Medium Hack application. It allows users to fetch and follow other users on the Medium platform.

Usage:
- Enter your authentication details when prompted.
- Choose whether to use a previous authentication token if available.
- Fetch and display the followers and following lists for specified usernames.
- Follow users based on the fetched data.

"""
from main import GetUsersList
from secret.helper import JsonFileWriter, JsonFileReader
import secret.constants as constants
from follow import FollowUserList


class TheMediumHack:
    """
    A class for The Medium Hack application.

    Attributes:
        user_name (str): The username for authentication.
        target_user (str): The target username for data fetching.
        unique_header (str): The unique authentication token.
        follow_users_result (str): The result of following users.
    """

    def __init__(self):
        """
        Initialize TheMediumHack instance.
        """
        self.user_name = input(constants.INPUT_USERNAME)
        self.target_user = input(constants.INPUT_TARGET_USERNAME)

        previous_token = self.previous_token()
        if previous_token.file_data is not None:
            use_previous_token = input(constants.INPUT_IS_PREVIOUS_TOKEN)
            if use_previous_token.lower() == "yes":
                self.unique_header = previous_token.file_data
        else:
            self.unique_header = input(constants.INPUT_UNIQUE_TOKEN)
            self.save_token()

        self.follow_users_result = []

        self.get_followers_list(self.user_name, True)
        # True for getting Following List
        self.get_followers_list(self.target_user, False)
        # False for getting Following List
        self.follow_users_result = FollowUserList(self.unique_header)

    def previous_token(self) -> JsonFileReader:
        """
        Read and return the previous token from a JSON file.

        Returns:
            JsonFileReader: An instance of JsonFileReader.
        """
        return JsonFileReader(constants.PATH_UNIQUE_HEADER_FILE)

    def save_token(self):
        """Save the unique header token to a JSON file."""
        write_instance = JsonFileWriter(constants.PATH_UNIQUE_HEADER_FILE)
        write_instance.write_file(self.unique_header)

    def get_followers_list(self, username: str, is_self: bool):
        """
        Get the followers or following list for a given username.

        Args:
            username (str): The username for which to fetch the list.
            is_self (bool): Indicates whether to fetch the self-followers or following list.
        """
        users_list = GetUsersList(username, is_self)
        self.follow_users_result.append(users_list)

    def follow_users(self):
        """Print the result of following users."""
        for result in self.follow_users_result:
            print(result)


if __name__ == "__main__":
    app = TheMediumHack()
    app.follow_users()
