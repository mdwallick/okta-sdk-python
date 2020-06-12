import json
import os
import unittest
import urllib

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktasdk.UsersClient import UsersClient
from oktasdk.framework.OktaError import OktaError
from oktasdk.framework.Utils import Utils
from oktasdk.framework.Serializer import Serializer
from oktasdk.models.user.ActivationResponse import ActivationResponse
from oktasdk.models.user.LoginCredentials import LoginCredentials
from oktasdk.models.user.ResetPasswordToken import ResetPasswordToken
from oktasdk.models.user.TempPassword import TempPassword
from oktasdk.models.user.User import User
from oktasdk.models.usergroup.UserGroup import UserGroup


class UserLifecycleTest(unittest.TestCase):

    def setUp(self):
        self.client = UsersClient(base_url="https://mockta.com",
                                  api_token="abcdefg")

        with open("tests/data/user.json", "r") as file:
            self.user = file.read()

        self.user_json = Utils.deserialize(self.user, User)

        with open("tests/data/users.json", "r") as file:
            self.users = file.read()

        self.users_json = Utils.deserialize(self.users, User)

        with open("tests/data/user_groups.json", "r") as file:
            self.user_groups = file.read()

        self.user_groups_json = Utils.deserialize(self.user_groups, UserGroup)

        with open("tests/data/created_user.json", "r") as file:
            self.created_user = file.read()

        self.created_user_json = Utils.deserialize(self.created_user, User)

    def tearDown(self):
        pass

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_activate_user_in_staged_status_returns_ok(self, mock_post):
        user = self.created_user_json
        activation_response = """
        {
            "activationUrl": "https://subdomain.okta.com/welcome/XE6wE17zmphl3KqAPFxO",
            "activationToken": "XE6wE17zmphl3KqAPFxO"
        }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=activation_response)
        response = self.client.activate_user(user.id, send_email=False)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, ActivationResponse)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_activate_user_not_in_staged_status_raises_okta_error(self, mock_post):
        user = self.created_user_json
        activation_response = """
            {
                "errorCode": "E0000016",
                "errorSummary": "Activation failed because the user is already active",
                "errorLink": "E0000016",
                "errorId": "oaeXSgWaUtkTvm8Vj9dkWGKiA",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_403_FORBIDDEN, text=activation_response)

        with self.assertRaises(OktaError):
            response = self.client.activate_user(user.id, send_email=False)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_deactivate_user_not_in_deprovisioned_status_returns_ok(self, mock_post):
        user = self.created_user_json
        deactivation_response = "{}"
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=deactivation_response)
        response = self.client.deactivate_user(user.id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_deactivate_user_in_deprovisioned_status_raises_okta_error(self, mock_post):
        user = self.created_user_json
        deactivation_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=deactivation_response)

        with self.assertRaises(OktaError):
            response = self.client.deactivate_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_suspend_user_in_active_status_returns_ok(self, mock_post):
        user = self.created_user_json
        deactivation_response = "{}"
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=deactivation_response)
        response = self.client.suspend_user(user.id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_suspend_user_not_in_active_status_raises_okta_error(self, mock_post):
        user = self.created_user_json
        suspend_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: suspendUser",
                "errorLink": "E0000001",
                "errorId": "oaeEZ0YOffyTiKJMrfTUGdGMg",
                "errorCauses": [
                    {
                        "errorSummary": "Cannot suspend a user that is not active"
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=suspend_response)

        with self.assertRaises(OktaError):
            response = self.client.suspend_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_suspend_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        suspend_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=suspend_response)

        with self.assertRaises(OktaError):
            response = self.client.suspend_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unsuspend_user_in_suspend_status_returns_ok(self, mock_post):
        user = self.created_user_json
        unsuspend_response = "{}"
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=unsuspend_response)
        response = self.client.suspend_user(user.id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unsuspend_user_not_in_suspend_status_raises_okta_error(self, mock_post):
        user = self.created_user_json
        unsuspend_response = """
            {
                "errorCode": "E0000001",
                "errorSummary": "Api validation failed: suspendUser",
                "errorLink": "E0000001",
                "errorId": "oaeEZ0YOffyTiKJMrfTUGdGMg",
                "errorCauses": [
                    {
                        "errorSummary": "Cannot unsuspend a user that is not suspended"
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_400_BAD_REQUEST, text=unsuspend_response)

        with self.assertRaises(OktaError):
            response = self.client.suspend_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unsuspend_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        unsuspend_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=unsuspend_response)

        with self.assertRaises(OktaError):
            response = self.client.suspend_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unlock_user_in_locked_out_status_returns_ok(self, mock_post):
        user = self.created_user_json
        unlock_response = "{}"
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=unlock_response)
        response = self.client.unlock_user(user.id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unlock_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        unlock_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=unlock_response)

        with self.assertRaises(OktaError):
            response = self.client.suspend_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_unlock_user_not_in_locked_out_status_raises_okta_error(self, mock_post):
        user = self.created_user_json
        unlock_response = """
            {
                "errorCode": "E0000032",
                "errorSummary": "Unlock is not allowed for this user.",
                "errorLink": "E0000032",
                "errorId": "oaelf2h18-jTBW7wE8kDhC2-Q",
                "errorCauses": [
                    {
                        "errorSummary": "The user is not locked out."
                    }
                ]
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_403_FORBIDDEN, text=unlock_response)
        
        with self.assertRaises(OktaError):
            response = self.client.unlock_user(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_reset_password_returns_ok(self, mock_post):
        user = self.created_user_json
        reset_password_response = """
            {
                "resetPasswordUrl": "https://wallick.oktapreview.com/reset_password/drpGwLleDltyCLJHXlDx"
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=reset_password_response)
        response = self.client.reset_password(user.id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, ResetPasswordToken)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_reset_password_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        reset_password_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=reset_password_response)

        with self.assertRaises(OktaError):
            response = self.client.reset_password(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_change_password_returns_ok(self, mock_post):
        user = self.created_user_json
        change_password_response = """
            {
                "password": {},
                "recovery_question": {
                    "question": "What is the food you least liked as a child?"
                },
                "provider": {
                    "type": "OKTA",
                    "name": "OKTA"
                }
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=change_password_response)
        response = self.client.change_password(user.id, "oldpw", "newpw")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, LoginCredentials)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_change_recovery_question_returns_ok(self, mock_post):
        user = self.created_user_json
        change_recovery_question_response = """
            {
                "password": {},
                "recovery_question": {
                    "question": "What is the food you least liked as a child?"
                },
                "provider": {
                    "type": "OKTA",
                    "name": "OKTA"
                }
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=change_recovery_question_response)
        response = self.client.change_recovery_question(user.id, "password", "question", "answer")
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, LoginCredentials)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_expire_password_no_temp_password_returns_ok(self, mock_post):
        user = self.created_user_json
        expire_password_response = self.created_user
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=expire_password_response)
        response = self.client.expire_password(user.id)
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, TempPassword)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_expire_password_with_temp_password_returns_ok(self, mock_post):
        user = self.created_user_json
        expire_password_response = """
            {
                "tempPassword": "HR076gb6"
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=expire_password_response)
        response = self.client.expire_password(user.id, temp_password=True)
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, TempPassword)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_expire_password_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        expire_password_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=expire_password_response)

        with self.assertRaises(OktaError):
            response = self.client.expire_password(user.id)
            self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_reset_factors_returns_ok(self, mock_post):
        user = self.created_user_json
        reset_factor_response = "{}"
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=reset_factor_response)
        response = self.client.reset_factors(user.id)
        
        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_reset_factors_user_not_found_raises_okta_error(self, mock_post):
        user = self.created_user_json
        reset_factor_response = """
            {
                "errorCode": "E0000007",
                "errorSummary": "Not found: Resource not found: 00us1r8ltrdVHGEJU0h7 (User)",
                "errorLink": "E0000007",
                "errorId": "oaeQJJQ-IClRTay4IS780nTiQ",
                "errorCauses": []
            }
        """
        mock_post.return_value = Mock(
            status_code=status.HTTP_404_NOT_FOUND, text=reset_factor_response)

        with self.assertRaises(OktaError):
            response = self.client.reset_factors(user.id)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, User)
