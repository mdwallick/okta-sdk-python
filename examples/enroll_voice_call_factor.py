from oktasdk.UsersClient import UsersClient
from oktasdk.FactorsClient import FactorsClient
from oktasdk.framework.OktaError import OktaError
from script_config import base_url, api_token, user_id

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)

print("Enroll voice call factor started")
phone_number = input("Please enter your phone number (just numbers please): ")

try:
    response = factorsClient.enroll_call_factor(user_id, phone_number)
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
        print("Voice call factor enrolled")
    except OktaError as e:
        print(e.error_causes)
