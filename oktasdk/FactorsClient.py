from oktasdk.framework.ApiClient import ApiClient
from oktasdk.framework.Utils import Utils
from oktasdk.models.factor.FactorCatalogEntry import FactorCatalogEntry
from oktasdk.models.factor.Factor import Factor
from oktasdk.models.factor.Question import Question
from oktasdk.models.factor.FactorVerificationResponse import FactorVerificationResponse
from oktasdk.models.factor.FactorDevice import FactorDevice
from oktasdk.models.factor.ActivationResponse import ActivationResponse


class FactorsClient(ApiClient):

    def __init__(self, *args, **kwargs):
        kwargs['pathname'] = '/api/v1/users'
        ApiClient.__init__(self, *args, **kwargs)

    def get_factors_catalog(self, user_id):
        """Get available factors for a user

        :param user_id: target user id
        :type user_id: str
        :rtype: list of FactorCatalogEntry
        """
        response = ApiClient.get_path(
            self, '/{0}/factors/catalog'.format(user_id))
        return Utils.deserialize(response.text, FactorCatalogEntry)

    def get_lifecycle_factors(self, user_id):
        """Get enrolled factors for a user

        :param user_id: target user id
        :type user_id: str
        :rtype: list of Factor
        """
        response = ApiClient.get_path(self, '/{0}/factors'.format(user_id))
        return Utils.deserialize(response.text, Factor)

    # FACTOR CRUD

    def get_available_questions(self, user_id):
        """Get available factor questions

        :param user_id: target user id
        :type user_id: str
        :rtype: list of Question
        """
        response = ApiClient.get_path(
            self, '/{0}/factors/questions'.format(user_id))
        return Utils.deserialize(response.text, Question)

    def enroll_email_factor(self, user_id, email):
        """Enroll a user into the email factor

        :param user_id: target user id
        :type user_id: str
        :param email: the email address to enroll
        :type email: str
        """
        enroll_request = {
            "factorType": "email",
            "provider": "OKTA",
            "profile": {
                "email": email
            }
        }
        return self.enroll_factor(user_id, enroll_request)

    def enroll_sms_factor(self, user_id, phone_number, update_phone=False, activate=False):
        """Enroll a user into the SMS factor

        :param user_id: target user id
        :type user_id: str
        :param phone_number: the phone number to enroll
        :type phone_number: str
        """
        enroll_request = {
            "factorType": "sms",
            "provider": "OKTA",
            "profile": {
                "PhoneNumber": phone_number
            }
        }
        return self.enroll_factor(user_id, enroll_request, update_phone, activate)

    def enroll_call_factor(self, user_id, phone_number, update_phone=False, activate=False):
        """Enroll a user into the voice call factor

        :param user_id: target user id
        :type user_id: str
        :param phone_number: the phone number to enroll
        :type phone_number: str
        """
        enroll_request = {
            "factorType": "call",
            "provider": "OKTA",
            "profile": {
                "PhoneNumber": phone_number
            }
        }
        return self.enroll_factor(user_id, enroll_request, update_phone, activate)

    def enroll_google_authenticator_factor(self, user_id):
        """Enroll a user into the Google Authenticator factor

        :param user_id: target user id
        :type user_id: str
        """
        enroll_request = {
            "factorType": "token:software:totp",
            "provider": "GOOGLE"
        }
        return self.enroll_factor(user_id, enroll_request)

    def enroll_okta_otp_factor(self, user_id):
        """Enroll a user into the Okta Verify OTP factor

        :param user_id: target user id
        :type user_id: str
        """
        enroll_request = {
            "factorType": "token:software:totp",
            "provider": "OKTA"
        }
        return self.enroll_factor(user_id, enroll_request)

    def enroll_okta_push_factor(self, user_id):
        """Enroll a user into the Okta Verify Push factor

        :param user_id: target user id
        :type user_id: str
        """
        enroll_request = {
            "factorType": "push",
            "provider": "OKTA"
        }
        return self.enroll_factor(user_id, enroll_request)

    def push_activation_poll(self, url):
        """Poll for push enrollment activation

        :param url: push enrollment polling URL
        :type url: str
        :rtype: ActivationResponse
        """
        response = ApiClient.post(self, url)
        return Utils.deserialize(response.text, ActivationResponse)

    def enroll_question_factor(self, user_id, question, answer):
        """Enroll a user into the security question factor

        :param user_id: target user id
        :type user_id: str
        :param question: the security question
        :type question: str
        :param answer: the answer to the question
        :type answer: str
        """
        enroll_request = {
            "factorType": "question",
            "provider": "OKTA",
            "profile": {
                "question": question,
                "answer": answer
            }
        }
        return self.enroll_factor(user_id, enroll_request)

    def enroll_factor(self, user_id, factor_enroll_request, update_phone=False, activate=False):
        """Enroll a user into a factor 

        :param user_id: target user id
        :type user_id: str
        :param factor_enroll_request: the details to enroll the user
        :type factor_enroll_request: FactorEnrollRequest
        :param update_phone: whether to update the user's phone during enrollment
        :type update_phone: bool
        :param activate: whether to silently activate the factor without verification
        :type activate: bool
        :rtype: Factor
        """
        params = {
            'updatePhone': update_phone,
            'activate': activate
        }
        response = ApiClient.post_path(
            self, '/{0}/factors'.format(user_id), factor_enroll_request, params=params)
        return Utils.deserialize(response.text, Factor)

    def get_factor(self, user_id, user_factor_id):
        """Get information about an enrolled factor

        :param user_id: target user id
        :type user_id: str
        :param user_factor_id: target factor id
        :type user_factor_id: str
        :rtype: Factor
        """
        response = ApiClient.get_path(
            self, '/{0}/factors/{1}'.format(user_id, user_factor_id))
        return Utils.deserialize(response.text, Factor)

    def reset_factor(self, user_id, user_factor_id):
        """Reset an enrolled factor

        :param user_id: target user id
        :type user_id: str
        :param user_factor_id: target factor id
        :type user_factor_id: str
        :rtype: None
        """
        ApiClient.delete_path(
            self, '/{0}/factors/{1}'.format(user_id, user_factor_id))

    # FACTOR LIFECYCLE

    def activate_factor(self, user_id, user_factor_id, passcode):
        """Activate an enrolled factor

        :param user_id: target user id
        :type user_id: str
        :param user_factor_id: target factor id
        :type user_factor_id: str
        :param passcode: code required for activation
        :type passcode: str
        :rtype: Factor
        """
        request = {
            'passCode': passcode
        }
        response = ApiClient.post_path(
            self, '/{0}/factors/{1}/lifecycle/activate'.format(user_id, user_factor_id), request)
        return Utils.deserialize(response.text, Factor)

    def resend_code(self, user_id, user_factor_id):
        """Resend code for a factor

        :param user_id: target user id
        :type user_id: str
        :param user_factor_id: target factor id
        :type user_factor_id: str
        :return:
        """
        response = ApiClient.post_path(
            self, '/{0}/factors/{1}/resend'.format(user_id, user_factor_id))
        return Utils.deserialize(response.text, Factor)

    def verify_factor(self, user_id, user_factor_id, activation_token=None, answer=None, passcode=None):
        """Verify an enrolled factor

        :param user_id: target user id
        :type user_id: str
        :param user_factor_id: target factor id
        :type user_factor_id: str
        :param activation_token: token required for activation
        :type activation_token: str
        :param answer: answer usually required for a question factor
        :type answer: str
        :param passcode: code required for verification
        :type passcode: str
        :return:
        """
        request = {}
        if activation_token != None:
            request.update({'activation_token': activation_token})

        if answer != None:
            request.update({'answer': answer})

        if passcode != None:
            request.update({'passCode': passcode})

        response = ApiClient.post_path(
            self, '/{0}/factors/{1}/verify'.format(user_id, user_factor_id), request)
        return Utils.deserialize(response.text, FactorVerificationResponse)

    def push_verification_poll(self, url):
        """Poll for push verification

        :param url: push polling URL
        :type url: str
        :rtype: ActivationResponse
        """
        response = ApiClient.get(self, url)
        return Utils.deserialize(response.text, FactorVerificationResponse)
