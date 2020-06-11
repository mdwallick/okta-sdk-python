import json
import random

from okta.UsersClient import UsersClient
from okta.models.user.User import User
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from script_config import base_url, api_token

start_number = random.randrange(1, 1000, 1)
end_number = random.randrange(1, 1000, 1)

usersClient = UsersClient(
    base_url=base_url, api_token=api_token)

user = User(
    login="testuser{0}@mailinator.com".format(start_number),
    firstName="Test",
    lastName="User {0}".format(start_number),
    middleName="David",
    honorificPrefix="Mr.",
    honorificSuffix="Sr.",
    email="testuser{0}@mailinator.com".format(start_number),
    title="Some sort of job title",
    displayName="Not automated",
    nickName="Testy{0}".format(start_number),
    profileUrl="http://localhost",
    secondEmail="testuser{0}@mailinator.com".format(end_number),
    mobilePhone="9135551212",
    primaryPhone="9135551213",
    streetAddress="123 Main Street",
    city="Anytown",
    state="KS",
    zipCode="12345",
    countryCode="US",
    postalAddress="Different than street address?",
    locale="en_US",
    timezone="US/Central",
    userType="Okta",
    employeeNumber="123455677890",
    costCenter="Finance & Operations",
    organization="Thorax Studios",
    division="Operations",
    department="Information Technology",
    managerId="0987654321",
    manager="Manny McManager"
)

try:
    test_user = usersClient.create_user(user, activate=False)
    user_id = test_user.id
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
    exit(2)

print("Get User")
user = usersClient.get_user(user_id)
print("ID: {0}".format(user.id))
print("Status: {0}".format(user.status))
print("{0}\n".format(json.dumps(user.profile, cls=Serializer, indent=2)))

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
print("{0}\n".format(json.dumps(user.profile, cls=Serializer, indent=2)))

print("Suspend User")
print("only valid for a user that is ACTIVE")
print("this will raise an error because the user")
print("we created has not been activated")
try:
    user = usersClient.suspend_user(user_id)
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

print("Delete User\n")
usersClient.delete_user(user_id)

print("Try and get the user we just deleted")
print("This will raise an error")
try:
    user = usersClient.get_user(user_id)
    print(json.dumps(user.profile, cls=Serializer, indent=2))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
