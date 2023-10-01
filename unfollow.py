import requests
import json
import time

# Define the request headers
headers = {
    "Content-Type": "application/json",
    "Cookie": "ab.storage.deviceId.a9882122-ac6c-486a-bc3b-fab39ef624c5=%7B%22g%22%3A%22f8b15442-f247-62b2-778b-befa8249de0f%22%2C%22c%22%3A1684390516698%2C%22l%22%3A1684390516698%7D; nonce=66SSqGLQ; sid=1:T0vOUr4K0OVvLpJNWc1ObX6DHoYOquk0mIGlzKE0cYM7lj9RJWPQyceiHxZw9QUM; uid=92dbc9507834; optimizelyEndUserId=oeu1693202491514r0.752176246721113; _ga_6NMP4D2Z90=GS1.1.1693202491.1.0.1693202493.0.0.0; _ga=GA1.1.1737828531.1684390519; __cfruid=e4dcdfa29106fde6bcb0f04549cbd164c10a2d3b-1695218852; xsrf=20ac2acc9295; _ga_7JY7T788PK=GS1.1.1695219526.50.1.1695219573.0.0.0; _dd_s=rum=0&expire=1695220623514",
}

# Read the JSON file with user data
with open("user_followers.json", "r") as file:
    user_data = json.load(file)

# Define the API URL for following users
follow_url = "https://keentolearn.medium.com/_/graphql"

# Define the GraphQL query
graphql_query_template = {
    "key": "user.unfollowed",
    "data": {
        "targetUserId": "",
        "followSource": "user_following_list",
        "service": "lite",
        "location": "https://medium.com/@yashraj.lnwebworks/following",
        "browserWidth": 1006,
        "referrer": "https://medium.com/@yashraj.lnwebworks",
        "referrerSource": "blogrolls_sidebar---two_column_layout_sidebar----------------------------------",
    },
    "type": "e",
    "timestamp": int(time.time()),
    "eventId": "lms094xv1jhie67g5tn",
}


# Iterate through user data and send follow requests
for user in user_data:
    user_id = user.get("id")

    # Create a copy of the GraphQL query template
    graphql_query = dict(graphql_query_template)

    # Replace the targetUserId in the GraphQL query
    graphql_query["data"]["targetUserId"] = user_id

    # Send the API request
    response = requests.post(follow_url, headers=headers, json=[graphql_query])

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        # You can process the result here if needed

        # Example: Print the response
        print(f"Un-follow user with ID: {user_id}")

    else:
        # Print an error message if the request failed
        print(f"Request failed with status code {response.status_code}")
