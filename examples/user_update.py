import json
import random

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
from script_config import base_url, api_token, user_id

start_number = random.randrange(1, 1000, 1)
end_number = random.randrange(1, 1000, 1)

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)

print("Update User-partial update")
print("This will not erase attributes not present in the request")
updated_user = User(
    login=user.profile.login,
    firstName=user.profile.firstName,
    lastName="User {0}".format(end_number),
    email=user.profile.email
)
user = usersClient.update_user_by_id(user_id, updated_user, True)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print("{0}\n".format(json.dumps(user.profile, cls=Serializer, indent=2)))

print("Update User-full update")
print("This will erase any attribute not present in the request")
updated_user = User(
    login=user.profile.login,
    firstName=user.profile.firstName,
    lastName="User {0}".format(end_number),
    email=user.profile.email
)
user = usersClient.update_user_by_id(user_id, updated_user, False)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print("{0}".format(json.dumps(user.profile, cls=Serializer, indent=2)))
