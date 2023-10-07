import json

# Read the JSON file
with open("my_followers.json", "r") as file:
    my_data = json.load(file)

with open("target_followers.json", "r") as file:
    user_data = json.load(file)

# Count the number of records
my_records = len(my_data)
record_count = len(user_data)

# Print the record count
print(f"Total records: {my_records}")
print(f"Total records: {record_count}")
