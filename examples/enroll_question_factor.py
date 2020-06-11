from okta.UsersClient import UsersClient
from okta.FactorsClient import FactorsClient
from okta.framework.OktaError import OktaError
from script_config import base_url, api_token, user_id

usersClient = UsersClient(base_url=base_url, api_token=api_token)
factorsClient = FactorsClient(base_url=base_url, api_token=api_token)

user = usersClient.get_user(user_id)
available_questions = factorsClient.get_available_questions(user_id)

num = 1
for question in available_questions:
    print("{0}.) {1}".format(num, question.questionText))
    num = num + 1

chosen_number = int(input("\nPlease choose a question: "))
chosen_question = available_questions[chosen_number - 1]
question = chosen_question.question
answer = input("{0}: ".format(chosen_question.questionText))

enroll_request = {
    "factorType": "question",
    "provider": "OKTA",
    "profile": {
        "question": question,
        "answer": answer
    }
}

print("Enroll question factor started")
try:
    response = factorsClient.enroll_factor(user_id, enroll_request)
    print("Security question enrolled")
except OktaError as e:
    print(e.error_causes)
    exit(2)
