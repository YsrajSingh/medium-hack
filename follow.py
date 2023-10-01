import requests
import json
from secret.helper import JsonObjectReader

json_file = JsonObjectReader()
json_data = json_file.fetch_json_by_name("follow_users")

# Read the JSON file with user data
with open("user_followers.json", "r") as file:
    user_data = json.load(file)


# Define the GraphQL query
graphql_query_template = {
    "operationName": "FollowUserMutation",
    "variables": {"targetUserId": ""},  # To be replaced with user id from the file
    "query": "mutation FollowUserMutation($targetUserId: ID!) {\n  followUser(targetUserId: $targetUserId) {\n    __typename\n    id\n    name\n    viewerEdge {\n      __typename\n      id\n      isFollowing\n    }\n  }\n}\n",
}

# Iterate through user data and send follow requests
for user in user_data:
    user_id = user.get("id")

    # Create a copy of the GraphQL query template
    graphql_query = dict(graphql_query_template)

    # Replace the targetUserId in the GraphQL query
    graphql_query["variables"]["targetUserId"] = user_id

    # Send the API request
    response = requests.post(
        json_data["url"], headers=json_data["header"], json=[graphql_query]
    )

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # You can process the result here if needed

        # Example: Print the response
        print(f"Followed user with ID: {user_id}")

    else:
        # Print an error message if the request failed
        print(f"Request failed with status code {response.status_code}")
