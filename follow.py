from secret.helper import JsonObjectReader, JsonFileReader, ApiHandler
from secret import constants


class FollowUserList:
    def __init__(self, header_token):
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
                        f"{constants.ERROR_FAILED_WITH_STATUS_CODE} : {response_status} for {user_id} : {user.name}"
                    )
            else:
                print(
                    f"{user.name} {constants.ALREADY_FOLLOWED_YOU}, {constants.ID}: {user_id}"
                )

    def __str__(self):
        return f"{constants.COUNT_FOLLOWED_USERS}: {self.followed_count}"
