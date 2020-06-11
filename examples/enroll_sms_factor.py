from okta.UsersClient import UsersClient
from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from script_config import base_url, api_token, user_id

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)

print("Enroll SMS factor started")
phone_number = input("Please enter your phone number (just numbers please): ")
enroll_request = {
    "factorType": "sms",
    "provider": "OKTA",
    "profile": {
        "phoneNumber": phone_number
    }
}

try:
    response = factorsClient.enroll_factor(user_id, enroll_request)
    result = response.status
    factor_id = response.id
except OktaError as e:
    print(e.error_causes)
    exit(2)

while result == "PENDING_ACTIVATION":
    # active when done
    try:
        pass_code = input("Enter your OTP: ")
        response = factorsClient.activate_factor(user_id, factor_id, pass_code)
        result = response.status
        print("SMS factor enrolled")
    except OktaError as e:
        print(e.error_causes)
