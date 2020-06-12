import json

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
from script_config import base_url, api_token, user_id

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)

print("Suspend User")
print("only valid for a user that is ACTIVE")
try:
    usersClient.suspend_user(user_id)
    user = usersClient.get_user(user_id)
    print("ID: {0}".format(user.id))
    print("Status: {0}\n".format(user.status))
except OktaError as e:
    print(e.error_summary)
    print("{0}\n".format(e.error_causes))

print("Unsuspend User")
print("only valid for a user that is SUSPENDED")
try:
    usersClient.unsuspend_user(user_id)
    user = usersClient.get_user(user_id)
    print("ID: {0}".format(user.id))
    print("Status: {0}\n".format(user.status))
except OktaError as e:
    print(e.error_summary)
    print("{0}\n".format(e.error_causes))

print("Deactivate User")
usersClient.deactivate_user(user_id)
user = usersClient.get_user(user_id)
print("ID: {0}".format(user.id))
print("Status: {0}\n".format(user.status))

print("Reactivate User")
usersClient.activate_user(user_id)
user = usersClient.get_user(user_id)
print("ID: {0}".format(user.id))
print("Status: {0}\n".format(user.status))
