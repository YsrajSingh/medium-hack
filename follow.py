from secret.helper import JsonObjectReader, JsonFileReader, ApiHandler

json_object = JsonObjectReader()
target_file = JsonFileReader("data/target_followers.json")
json_data = json_object.fetch_json_by_name("follow_users")
api_handler = ApiHandler(json_data["url"], json_data["header"])

for user in target_file.file_data:
    user_id = user.get("id")
    json_data["body"]["variables"]["targetUserId"] = user_id
    response_status, response_data = api_handler.json_call_handler(json_data["body"])
    if response_status == 200 and response_data:
        print(f"Followed user with ID: {user_id}")
    else:
        print(f"Request failed with status code {user_id}")
