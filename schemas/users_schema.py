def user_serializer(user) -> dict:
    return {
        "_id": user["_id"],
        "username": user["username"],
        "password": user["password"],
        "realname": user["realname"],
        "clubs": user["clubs"],
        "refresh_token": user["refresh_token"],
        "authority": user["authority"],
        "interests": user["interests"]
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]