from main import GetUsersList


user_name = input("Enter Your Username:")
target_user = input("Enter Target Username:")

GetUsersList(user_name, True)
GetUsersList(target_user, False)
