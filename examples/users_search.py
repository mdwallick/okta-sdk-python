import json

from okta.UsersClient import UsersClient
from okta.models.user.User import User
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from script_config import base_url, api_token

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

print("Search users...")
try:
    # set a low limit to guarantee we get at least 2 pages of results
    users = usersClient.get_paged_users(limit=2)
    pageNo = 1
    while not users.is_last_page():
        print("Page number {0}".format(pageNo))
        
        for user in users.result:
            print("{0} {1}".format(user.profile.firstName, user.profile.lastName))
        
        if not users.is_last_page():
            users = usersClient.get_paged_users(url=users.next_url)
            pageNo = pageNo + 1

except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)


print("get_users with filter...")
users = usersClient.get_users(query="you won't find this")
print(json.dumps(users, cls=Serializer, indent=2))
print("Found {0} users".format(len(users)))
