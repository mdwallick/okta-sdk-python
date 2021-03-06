import json
import os
import unittest
import urllib

from flask_api import status
from unittest.mock import Mock, patch
from okta.UsersClient import UsersClient
from okta.framework.Utils import Utils
from okta.framework.Serializer import Serializer
from okta.models.user.User import User
from okta.models.usergroup.UserGroup import UserGroup


class UsersClientTest(unittest.TestCase):

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

    @patch("okta.framework.ApiClient.requests.post")
    def test_create_new_user_returns_ok(self, mock_post):
        user = self.created_user_json
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.created_user)
        response = self.client.create_user(user)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)
        #self.assertEqual(response.status, "STAGED")

    @patch("okta.framework.ApiClient.requests.post")
    def test_update_user_partial_update_returns_ok(self, mock_post):
        user = self.created_user_json
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.created_user)
        response = self.client.update_user(user, partial=True)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)
        #self.assertEqual(response.status, "STAGED")

    @patch("okta.framework.ApiClient.requests.put")
    def test_update_user_full_update_returns_ok(self, mock_put):
        user = self.created_user_json
        mock_put.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.created_user)
        response = self.client.update_user(user, partial=False)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)
        #self.assertEqual(response.status, "STAGED")

    @patch("okta.framework.ApiClient.requests.delete")
    def test_delete_user_returns_ok(self, mock_delete):
        user_id = self.user_json.id
        mock_delete.return_value = Mock(
            status_code=status.HTTP_202_ACCEPTED, text="{}")
        response = self.client.delete_user(user_id)

        self.assertIsNotNone(response)

    @patch("okta.framework.ApiClient.requests.get")
    def test_get_users_returns_ok(self, mock_get):
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.users)
        response = self.client.get_users()

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(self.users_json))
        self.assertIsInstance(response[0], User)

    @patch("okta.framework.ApiClient.requests.get")
    def test_get_user_by_id_returns_ok(self, mock_get):
        user_id = self.user_json.id
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.user)
        response = self.client.get_user(user_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, User)
        self.assertEqual(response.id, user_id)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_limit_returns_ok(self, mock_get):
        limit = 2
        # is it a valid test to manipulate the return data from a mocked function?
        filtered_users = json.loads(self.users)
        # just get the first 2 users
        filtered_users = filtered_users[0:2]
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(limit=limit)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(len(response), limit)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_query_first_name_returns_ok(self, mock_get):
        # query supports searching by first name, last name and emails
        query = "Gordon"
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(query=query)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(query, response[0].profile.firstName)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_query_last_name_returns_ok(self, mock_get):
        # query supports searching by first name, last name and emails
        query = "Sumner"
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(query=query)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(query, response[0].profile.lastName)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_query_primary_email_returns_ok(self, mock_get):
        # query supports searching by first name, last name and emails
        query = "gordon@mailinator.com"
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(query=query)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(query, response[0].profile.email)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_query_secondary_email_returns_nothing(self, mock_get):
        # query supports searching by first name, last name and emails
        query = "sting@mailinator.com"
        filtered_users = "[]"
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(query=query)

        self.assertIsNotNone(response)
        self.assertEqual(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_status_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        filter_string = urllib.parse.quote_plus("status eq \"ACTIVE\"")
        filtered_users = self.users
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        # 5 users in the test data that are active
        self.assertEqual(len(response), 5)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].status, "ACTIVE")

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_lastUpdated_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        filter_string = urllib.parse.quote_plus(
            "lastUpdated gt \"2019-12-17T00:00:00.000Z\"")
        filtered_users = self.users
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 5)
        self.assertIsInstance(response[0], User)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_id_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        user_id = self.user_json.id
        filter_string = urllib.parse.quote_plus(
            "id eq \"{0}\"".format(user_id))
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].id, user_id)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_login_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        login = "gordon@mailinator.com"
        filter_string = urllib.parse.quote_plus(
            "profile.login eq \"{0}\"".format(login))
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].profile.login, login)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_email_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        email = "gordon@mailinator.com"
        filter_string = urllib.parse.quote_plus(
            "profile.email eq \"{0}\"".format(email))
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].profile.email, email)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_first_name_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        first_name = "Gordon"
        filter_string = urllib.parse.quote_plus(
            "profile.firstName eq \"{0}\"".format(first_name))
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].profile.firstName, first_name)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_list_users_with_filter_by_last_name_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # status, lastUpdated, id, profile.login, profile.email,
        # profile.firstName, and profile.lastName
        last_name = "Sumner"
        filter_string = urllib.parse.quote_plus(
            "profile.lastName eq \"{0}\"".format(last_name))
        filtered_users = json.loads("[{0}]".format(self.user))
        filtered_users = json.dumps(filtered_users)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_users)
        response = self.client.get_users(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(response[0].profile.lastName, last_name)
        self.assertGreater(len(response), 0)

    @patch("okta.framework.ApiClient.requests.get")
    def test_get_user_groups_returns_ok(self, mock_get):
        user_id = self.user_json.id
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.user_groups)
        response = self.client.get_user_groups(user_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], UserGroup)
        self.assertEqual(len(response), 3)
