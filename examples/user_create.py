import json
import random

from oktasdk.UsersClient import UsersClient
from oktasdk.models.user.User import User
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Serializer import Serializer
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
    created_user = usersClient.create_user(user)
    print("ID: {0}".format(created_user.id))
    print("Status: {0}".format(created_user.status))
    print("{0}".format(json.dumps(created_user.profile, cls=Serializer, indent=2)))
except OktaError as e:
    print(e.error_summary)
    print(e.error_causes)
