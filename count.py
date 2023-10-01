import json

# Read the JSON file
with open("user_followers.json", "r") as file:
    user_data = json.load(file)

# Count the number of records
record_count = len(user_data)

# Print the record count
print(f"Total records: {record_count}")
