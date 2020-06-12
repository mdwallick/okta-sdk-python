import json

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
from script_config import base_url, api_token, user_id

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

try:
    print("Get User")
    user = usersClient.get_user(user_id)
    print("ID: {0}".format(user.id))
    print("Status: {0}".format(user.status))
    print("{0}\n".format(json.dumps(user.profile, cls=Serializer, indent=2)))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
