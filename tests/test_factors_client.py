import unittest
import os
import json

from flask_api import status
from unittest.mock import Mock, patch
from oktasdk.FactorsClient import FactorsClient
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Utils import Utils
from oktasdk.framework.Serializer import Serializer
from oktasdk.models.factor.Factor import Factor
from oktasdk.models.factor.FactorCatalogEntry import FactorCatalogEntry
from oktasdk.models.factor.Question import Question


class FactorsClientTest(unittest.TestCase):

    def setUp(self):
        self.client = FactorsClient(base_url="https://mockta.com",
                                    api_token="abcdefg")
        self.user_id = "00upofwtwaGmrmIsm0h7"
        self.factor_id = "ufss082hlipGNzCff0h7"

        with open("tests/data/factor.json", "r") as file:
            self.factor = file.read()

        with open("tests/data/factors.json", "r") as file:
            self.factors = file.read()

        with open("tests/data/enrolled_factor.json", "r") as file:
            self.enrolled_factor = file.read()
        
        with open("tests/data/available_factors.json", "r") as file:
            self.available_factors = file.read()

        with open("tests/data/available_questions.json", "r") as file:
            self.available_questions = file.read()

    def tearDown(self):
        pass

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_enrolled_factors(self, mock_get):
        # Configure the mock to return a response with an OK status code
        # and the raw text response (unparsed JSON)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.factors)
        response = self.client.get_lifecycle_factors(self.user_id)
        factor_json = Utils.deserialize(self.factors, Factor)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(factor_json))
        self.assertIsInstance(response[0], Factor)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_factor_by_id(self, mock_get):
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.factor)
        response = self.client.get_factor(self.user_id, self.factor_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)
        self.assertEqual(response.id, self.factor_id)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_available_factors(self, mock_get):
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.available_factors)
        response = self.client.get_factors_catalog(self.user_id)
        factor_json = Utils.deserialize(self.available_factors, FactorCatalogEntry)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(factor_json))
        self.assertIsInstance(response[0], FactorCatalogEntry)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_available_questions(self, mock_get):
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.available_questions)
        response = self.client.get_available_questions(self.user_id)
        factor_json = Utils.deserialize(self.available_questions, Question)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(factor_json))
        self.assertIsInstance(response[0], Question)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_email_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_email_factor(
            self.user_id, "testuser1@mailinator.com")

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_email_factor_with_unverified_email_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: Only verified primary or secondary email can be enrolled.",
                "errorLink": "E0000001",
                "errorId": "oaezMG94PbVSw-joFMvwEQ93w",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            response = self.client.enroll_email_factor(
                self.user_id, "testuser1@mailinator.com")
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_email_factor_with_enrolled_email_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_email_factor(
                self.user_id, "testuser1@mailinator.com")
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_sms_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_sms_factor(self.user_id, "9135551212")

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_sms_factor_with_new_number_raises_okta_error(self, mock_post):
        # trying to enroll a new phone number when there is already a verified
        # number raises and OktaError unless update_phone == true
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oaei_FUQRnlS8aDaNv0ZnHuGw",
                "errorCauses": [
                    {
                        "errorSummary": "There is an existing verified phone number."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            response = self.client.enroll_sms_factor(
                self.user_id, "9135551212")
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_sms_factor_with_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_sms_factor(
                self.user_id, "9135551212")
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_call_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_call_factor(self.user_id, "9135551212")

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_call_factor_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_call_factor(
                self.user_id, "9135551212")
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_google_authenticator_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_google_authenticator_factor(self.user_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_google_authenticator_factor_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_google_authenticator_factor(
                self.user_id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_okta_verify_otp_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_okta_otp_factor(self.user_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_okta_verify_otp_factor_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_okta_otp_factor(self.user_id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_okta_verify_push_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_okta_push_factor(self.user_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_okta_verify_push_factor_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_okta_push_factor(self.user_id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_question_factor_returns_ok(self, mock_post):
        enroll_response = self.enrolled_factor
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=enroll_response)
        response = self.client.enroll_question_factor(
            self.user_id, "question", "answer")

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_enroll_question_factor_already_enrolled_raises_okta_error(self, mock_post):
        enroll_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: factorEnrollRequest",
                "errorLink": "E0000001",
                "errorId": "oae2sBU0ZgRTXmVtaXIE5nOVA",
                "errorCauses": [
                    {
                        "errorSummary": "A factor of this type is already set up."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=enroll_response)

        with self.assertRaises(OktaError):
            # Okta API will return HTTP 400
            response = self.client.enroll_question_factor(
                self.user_id, "question", "answer")
            self.assertIsNotNone(response)
