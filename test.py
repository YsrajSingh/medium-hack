import json

with open("secret/config.json") as f:
    data = json.load(f)

print(data["follow_users"])
