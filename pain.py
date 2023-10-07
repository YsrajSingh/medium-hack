from secret.helper import JsonObjectReader, JsonFileWriter, ApiHandler


class GetFollowingList:
    def __init__(self, user_name, optional):
        self.user_name = user_name
        self.is_optional = optional
        self.all_user_data = []
        self.json_file = JsonObjectReader()
        self.json_write_file = JsonFileWriter(
            "data/my_followers.json"
            if self.is_optional
            else "data/target_followers.json"
        )
        self.response = self.fetch_data()

    def __str__(self):
        return str(self.response)

    def optional(self, data):
        if self.is_optional:
            if isinstance(data, dict):
                return data.get("id")
            elif isinstance(data, list) and data:
                return data[0].get("id")

    def setup_api_request(self):
        self.json_data = self.json_file.fetch_json_by_name("fetch_following_list")
        self.json_data["body"]["variables"]["username"] = self.user_name
        self.json_data["body"]["variables"]["id"] = self.json_data["body"]["variables"][
            "paging"
        ]["from"] = None
        self.api_handler = ApiHandler(self.json_data["url"], self.json_data["header"])

    def initial_data(self):
        self.setup_api_request()
        response_status, response_data = self.api_handler.json_call_handler(
            self.json_data["body"]
        )

        if response_status == 200 and response_data:
            initial_users = response_data["data"]["userResult"][
                "followingUserConnection"
            ]["users"]
            for user in initial_users:
                self.all_user_data.append(user["id"])

            return response_data["data"]["userResult"]["followingUserConnection"][
                "pagingInfo"
            ]["next"]["from"]

    def fetch_data(self):
        from_user_id = self.initial_data()
        while from_user_id:
            print("Loading")
            self.json_data["body"]["variables"]["paging"]["from"] = from_user_id
            response_status, response_data = self.api_handler.json_call_handler(
                self.json_data["body"]
            )
            if response_data is None:
                print("Error: API response is None")
                break
            if response_status == 200 and response_data:
                new_result = response_data
                user_data = new_result["data"]["userResult"]["followingUserConnection"][
                    "users"
                ]
                if self.is_optional:
                    user_ids = [user.get("id") for user in user_data if user.get("id")]
                    self.all_user_data.extend(user_ids)
                else:
                    self.all_user_data.extend(user_data)
                paging_info = response_data["data"]["userResult"][
                    "followingUserConnection"
                ]["pagingInfo"]
                next_data = paging_info.get("next")
                if next_data:
                    from_user_id = next_data.get("from")
                else:
                    from_user_id = None

        if self.all_user_data:
            self.json_write_file.write_file(self.all_user_data)
        return "Data fetching completed"
