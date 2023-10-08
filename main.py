from secret.helper import JsonObjectReader, JsonFileWriter, ApiHandler
import secret.constants as constants


class GetUsersList:
    def __init__(self, user_name, optional):
        self.user_name = user_name
        self.is_optional = optional
        self.all_user_data = []
        self.json_file = JsonObjectReader()
        self.json_write_file = JsonFileWriter(
            constants.PATH_USER_FILE if self.is_optional else constants.PATH_TARGET_FILE
        )
        self.response = self.fetch_data()

    def __str__(self):
        return str(self.response)

    def optional(self, data):
        if self.is_optional:
            if isinstance(data, dict):
                return data.get(constants.ID)
            elif isinstance(data, list) and data:
                return data[0].get(constants.ID)

    def setup_api_request(self):
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

    def initial_data(self):
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

    def fetch_data(self):
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
