import json

# Read all JSON files
with open("my_followers.json", "r") as file:
    my_data = json.load(file)

with open("target_followers.json", "r") as file:
    user_data = json.load(file)

# Count the number of records
my_followers_count = len(my_data)
target_followers_count = len(user_data)

# Print the record count
print(f"Total records: {my_followers_count}")
print(f"Total records: {target_followers_count}")
