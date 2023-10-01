import requests
import json
from secret.helper import JsonObjectReader

json_file = JsonObjectReader()
json_data = json_file.fetch_json_by_name("fetch_user_unique_id")

print(json_data["body"])
# Replace the targetUserId in the GraphQL query
# graphql_query["variables"]["targetUserId"] = user_id

# # Send the API request
# response = requests.post(
#     json_data["url"], headers=json_data["header"], json=[graphql_query]
# )

# # Check if the request was successful
# if response.status_code == 200:
#     result = response.json()
#     # You can process the result here if needed

#     # Example: Print the response
#     print(f"Followed user with ID: {user_id}")

# else:
#     # Print an error message if the request failed
#     print(f"Request failed with status code {response.status_code}")
