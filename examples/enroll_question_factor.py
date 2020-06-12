from oktasdk.UsersClient import UsersClient
from oktasdk.FactorsClient import FactorsClient
from oktasdk.framework.OktaError import OktaError
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

print("Enroll question factor started")
try:
    response = factorsClient.enroll_question_factor(user_id, question, answer)
    print("Security question enrolled")
except OktaError as e:
    print(e.error_causes)
    exit(2)