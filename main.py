import requests
import json
import os
from secret.helper import JsonObjectReader, JsonFileWriter

json_file = JsonObjectReader()
json_write_file = JsonFileWriter("data/user_followers.json")
json_data = json_file.fetch_json_by_name("fetch_followers_list")

# Initialize an empty list to store user data
all_user_data = []

# Initialize the starting "from" id
from_id = "148ae689f366"


while from_id:
    # Define the request body with the current "from" id
    data = {
        "operationName": "UserFollowers",
        "query": "query UserFollowers($username: ID, $id: ID, $paging: PagingOptions) {\n  userResult(username: $username, id: $id) {\n    __typename\n    ... on User {\n      id\n      followersUserConnection(paging: $paging) {\n        pagingInfo {\n          next {\n            from\n            limit\n            __typename\n          }\n          __typename\n        }\n        users {\n          ...FollowList_publisher\n          __typename\n        }\n        __typename\n      }\n      ...UserCanonicalizer_user\n      ...FollowersHeader_publisher\n      ...NoFollows_publisher\n      __typename\n    }\n  }\n}\n\nfragment FollowList_publisher on Publisher {\n  id\n  ... on Collection {\n    ...PublicationFollowRow_collection\n    __typename\n    id\n  }\n  ... on User {\n    ...UserFollowRow_user\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment PublicationFollowRow_collection on Collection {\n  id\n  name\n  description\n  ...CollectionAvatar_collection\n  ...CollectionFollowButton_collection\n  __typename\n}\n\nfragment CollectionAvatar_collection on Collection {\n  name\n  avatar {\n    id\n    __typename\n  }\n  ...collectionUrl_collection\n  __typename\n  id\n}\n\nfragment collectionUrl_collection on Collection {\n  id\n  domain\n  slug\n  __typename\n}\n\nfragment CollectionFollowButton_collection on Collection {\n  __typename\n  id\n  name\n  slug\n  ...collectionUrl_collection\n  ...SusiClickable_collection\n}\n\nfragment SusiClickable_collection on Collection {\n  ...SusiContainer_collection\n  __typename\n  id\n}\n\nfragment SusiContainer_collection on Collection {\n  name\n  ...SignInOptions_collection\n  ...SignUpOptions_collection\n  __typename\n  id\n}\n\nfragment SignInOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_collection on Collection {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowRow_user on User {\n  id\n  name\n  bio\n  ...UserAvatar_user\n  ...UserFollowButton_user\n  ...useIsVerifiedBookAuthor_user\n  __typename\n}\n\nfragment UserAvatar_user on User {\n  __typename\n  id\n  imageId\n  mediumMemberAt\n  membership {\n    tier\n    __typename\n    id\n  }\n  name\n  username\n  ...userUrl_user\n}\n\nfragment userUrl_user on User {\n  __typename\n  id\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  hasSubdomain\n  username\n}\n\nfragment UserFollowButton_user on User {\n  ...UserFollowButtonSignedIn_user\n  ...UserFollowButtonSignedOut_user\n  __typename\n  id\n}\n\nfragment UserFollowButtonSignedIn_user on User {\n  id\n  name\n  __typename\n}\n\nfragment UserFollowButtonSignedOut_user on User {\n  id\n  ...SusiClickable_user\n  __typename\n}\n\nfragment SusiClickable_user on User {\n  ...SusiContainer_user\n  __typename\n  id\n}\n\nfragment SusiContainer_user on User {\n  ...SignInOptions_user\n  ...SignUpOptions_user\n  __typename\n  id\n}\n\nfragment SignInOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment SignUpOptions_user on User {\n  id\n  name\n  __typename\n}\n\nfragment useIsVerifiedBookAuthor_user on User {\n  verifications {\n    isBookAuthor\n    __typename\n  }\n  __typename\n  id\n}\n\nfragment UserCanonicalizer_user on User {\n  id\n  username\n  hasSubdomain\n  customDomainState {\n    live {\n      domain\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment FollowersHeader_publisher on Publisher {\n  id\n  name\n  ... on Collection {\n    subscriberCount\n    ...collectionUrl_collection\n    __typename\n    id\n  }\n  ... on User {\n    socialStats {\n      followerCount\n      __typename\n    }\n    ...userUrl_user\n    __typename\n    id\n  }\n  __typename\n}\n\nfragment NoFollows_publisher on Publisher {\n  id\n  name\n  __typename\n}\n",
        "variables": {
            "id": "7278e7904835",
            "paging": {"from": from_id, "limit": 25},
            "username": None,
        },
    }

    # Make the API request
    response = requests.post(json_data["url"], headers=json_data["header"], json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse and extract user data from the response
        result = response.text
        new_result = json.loads(result)
        user_data = new_result["data"]["userResult"]["followersUserConnection"]["users"]
        print(user_data)
        # Append the user data to the list
        all_user_data.extend(user_data)

        # Get the "from" id from the last user in the response
        if user_data:
            from_id = user_data[-1]["id"]
        else:
            from_id = None

    else:
        # Print an error message if the request failed
        print(f"Request failed with status code {response.status_code}")

json_write_file.write_file(all_user_data)

# Process completed when from_id is None
print("Data fetching completed.")
