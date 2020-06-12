import json

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
from script_config import base_url, api_token, user_id

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

print("Delete User\n")
print("If a user is active, delete must be called twice")
print("Once to deactivate the user, and once to actually delete the user")
usersClient.delete_user(user_id)
usersClient.delete_user(user_id)

print("Try and get the user we just deleted")
print("This will raise an error")
try:
    user = usersClient.get_user(user_id)
    print(json.dumps(user.profile, cls=Serializer, indent=2))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
