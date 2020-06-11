from okta.UsersClient import UsersClient
from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from script_config import api_token, base_url, user_id, get_factor_id_by_type

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)
factors = factorsClient.get_lifecycle_factors(user.id)
factor_id, factor_profile = get_factor_id_by_type(factors, "call")

if factor_id == None:
    print("No voice call factor enrolled")
    exit(2)

print("Issuing Voice Call challenge: {0}".format(factor_profile.phoneNumber))

# issue the challenge
response = factorsClient.verify_factor(user.id, factor_id)
result = response.factorResult

while result != "SUCCESS":
    try:
        pass_code = input("Enter your OTP: ")
        response = factorsClient.verify_factor(
            user.id, factor_id, passcode=pass_code)
        result = response.factorResult
        print("Voice call verification passed")
    except OktaError as e:
        print(e.error_causes)
