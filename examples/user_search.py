import urllib

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
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
            print("{0} {1}\n".format(
                user.profile.firstName, user.profile.lastName))

        if not users.is_last_page():
            users = usersClient.get_paged_users(url=users.next_url)
            pageNo = pageNo + 1
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)

query = "gordon@mailinator.com"
print("get_users with query: {0}".format(query))
users = usersClient.get_users(query=query)
print("Found {0} users".format(len(users)))
for user in users:
    print("{0}: {1} {2} ({3})\n".format(user.id, user.profile.firstName,
                                        user.profile.lastName, user.profile.login))

filter_string = "status eq \"PROVISIONED\""
print("search with filter: {0}".format(filter_string))
filter_string = urllib.parse.quote_plus(filter_string)
users = usersClient.get_users(filter_string=filter_string)
for user in users:
    print("{0}: {1} {2} ({3})\n".format(user.id, user.profile.firstName,
                                        user.profile.lastName, user.profile.login))
