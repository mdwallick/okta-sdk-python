import json
import time

from okta.UsersClient import UsersClient
from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from okta.framework.Serializer import Serializer
from script_config import api_token, base_url, user_id, get_factor_id_by_type

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)
factors = factorsClient.get_lifecycle_factors(user.id)
factor_id, factor_profile = get_factor_id_by_type(factors, "push")

if factor_id == None:
    print("No Okta Verify Push factor enrolled")
    exit(2)

print("Issuing Okta Verify Push challenge: {0}".format(factor_profile.name))

# issue the challenge
response = factorsClient.verify_factor(user.id, factor_id)
result = response.factorResult
polling_url = response.links.get("poll").href

while result == "WAITING":
    try:
        response = factorsClient.push_verification_poll(polling_url)
        result = response.factorResult
        if result == "WAITING":
            print("Waiting for push verification")
            time.sleep(3)
        elif result == "SUCCESS":
            print("Push factor verification passed")
        elif result == "REJECTED":
            print("Push factor verification rejected by user")
        elif result == "TIMEOUT":
            print("Push factor verification timed out")
        else:
            print(json.dumps(response, cls=Serializer, indent=2))
            exit(2)
    except OktaError as e:
        print(e)
