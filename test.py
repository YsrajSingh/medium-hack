from main import GetUsersList
from follow import FollowUserList
from pain import GetFollowingList
from secret.helper import JsonFileWriter, JsonFileReader


class TheMediumHack:
    def __init__(self):
        self.user_name = input("Enter Your Username:")
        self.target_user = input("Enter Target Username:")

        previous_token = self.previous_token()
        if previous_token.file_data is not None:
            use_previous_token = input("Want to use Previous token (yes/no) :")
            if use_previous_token.lower() == "yes":
                self.unique_header = previous_token.file_data
        else:
            self.unique_header = input("Enter Your Unique Token:")
            self.save_token()
        self.get_following_list(self.user_name, True)
        # True for getting Following List
        self.get_followers_list(self.target_user, False)
        # False for getting Following List
        self.follow_users_result = FollowUserList(self.unique_header)

    def previous_token(self):
        return JsonFileReader("data/unique_header.json")

    def save_token(self):
        write_instance = JsonFileWriter("data/unique_header.json")
        write_instance.write_file(self.unique_header)

    def get_followers_list(self, username, is_self):
        GetUsersList(username, is_self)

    def get_following_list(self, username, is_self):
        GetFollowingList(username, is_self)

    def follow_users(self):
        print(self.follow_users_result)


if __name__ == "__main__":
    app = TheMediumHack()
    app.follow_users()
