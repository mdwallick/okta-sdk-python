import getpass
import json

from okta.UsersClient import UsersClient
from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from script_config import api_token, base_url, user_id, get_factor_id_by_type

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)
factors = factorsClient.get_lifecycle_factors(user.id)
factor_id, factor_profile = get_factor_id_by_type(factors, "question")

if factor_id == None:
    print("No Security Question factor enrolled")
    exit(2)

print("Verifying security question")
question = factor_profile.questionText
result = "WAITING"

while result != "SUCCESS":
    try:
        answer = getpass.getpass("{0}: ".format(question))
        response = factorsClient.verify_factor(user.id, factor_id, answer=answer)
        result = response.factorResult
        print("Security question verification passed")
    except OktaError as e:
        print(e.error_causes)
