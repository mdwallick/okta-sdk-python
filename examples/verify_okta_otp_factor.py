from oktasdk.UsersClient import UsersClient
from oktasdk.FactorsClient import FactorsClient
from oktasdk.framework.OktaError import OktaError
from script_config import api_token, base_url, user_id, get_factor_id_by_type

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)
factors = factorsClient.get_lifecycle_factors(user.id)
factor_id, factor_profile = get_factor_id_by_type(factors, "token:software:totp")

if factor_id == None:
    print("No Okta Verify OTP factor enrolled")
    exit(2)

print("Verifying Okta Verify OTP...")
result = "WAITING"

while result != "SUCCESS":
    try:
        pass_code = input("Enter your OTP: ")
        response = factorsClient.verify_factor(user_id, factor_id, passcode=pass_code)
        result = response.factorResult
        print("Okta Verify OTP verification passed")
    except OktaError as e:
        print(e.error_causes)
