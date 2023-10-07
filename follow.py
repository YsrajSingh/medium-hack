from secret.helper import JsonObjectReader, JsonFileReader, ApiHandler


class FollowUserList:
    def __init__(self, header_token):
        self.json_object = JsonObjectReader()
        self.target_file = JsonFileReader("data/target_followers.json")
        self.my_followers_file = JsonFileReader("data/my_followers.json")
        self.json_data = self.json_object.fetch_json_by_name("follow_users")
        self.json_data["header"]["Cookie"] = header_token
        self.api_handler = ApiHandler(self.json_data["url"], self.json_data["header"])
        self.followed_count = 0
        self.follow_users()

    def follow_users(self):
        for user in self.target_file.file_data:
            if self.followed_count >= 150:
                print("Follow limit reached. Exiting.")
                break
            user_id = user.get("id")
            if user_id not in self.my_followers_file.file_data:
                self.json_data["body"]["variables"]["targetUserId"] = user_id
                response_status, response_data = self.api_handler.json_call_handler(
                    self.json_data["body"]
                )
                if response_status == 200 and response_data:
                    self.followed_count += 1
                    print(f"Followed user with ID: {user_id}")
                else:
                    print(
                        f"Request failed with status code {response_status} for {user_id} : {user.name}"
                    )
            else:
                print(f"{user.name} Already Followed you, id: {user_id}")

    def __str__(self):
        return f"JsonDataManager: {self.followed_count} target users"
