import json
import os
import unittest
import urllib

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktasdk.UserGroupsClient import UserGroupsClient
from oktasdk.framework.Utils import Utils
from oktasdk.framework.Serializer import Serializer
from oktasdk.models.user.User import User
from oktasdk.models.usergroup.UserGroup import UserGroup
from .testutils import json_compare


class UserGroupTest(unittest.TestCase):

    def setUp(self):
        self.client = UserGroupsClient(base_url="https://mockta.com",
                                       api_token="abcdefg")

        with open("tests/data/group.json", "r") as file:
            self.group = file.read()

        self.group_json = Utils.deserialize(self.group, UserGroup)

        with open("tests/data/groups.json", "r") as file:
            self.groups = file.read()

        self.groups_json = Utils.deserialize(self.groups, UserGroup)

        with open("tests/data/created_group.json", "r") as file:
            self.created_group = file.read()

        self.created_group_json = Utils.deserialize(
            self.created_group, UserGroup)

        with open("tests/data/group_users.json", "r") as file:
            self.group_users = file.read()

        self.group_users_json = Utils.deserialize(
            self.group_users, User)

    def tearDown(self):
        pass

    @patch("oktasdk.framework.ApiClient.requests.post")
    def test_create_new_group_returns_ok(self, mock_post):
        group = self.created_group_json
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.created_group)
        response = self.client.create_group(group)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, UserGroup)

    @patch("oktasdk.framework.ApiClient.requests.put")
    def test_update_group_returns_ok(self, mock_post):
        group = self.created_group_json
        mock_post.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.created_group)
        response = self.client.update_group(group)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, UserGroup)
        #self.assertEqual(response.status, "STAGED")

    @patch("oktasdk.framework.ApiClient.requests.delete")
    def test_delete_group_returns_ok(self, mock_delete):
        group_id = self.group_json.id
        mock_delete.return_value = Mock(
            status_code=status.HTTP_202_ACCEPTED, text="{}")
        response = self.client.delete_group(group_id)

        self.assertIsNotNone(response)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_groups_returns_ok(self, mock_get):
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.groups)
        response = self.client.get_groups()

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(self.groups_json))
        self.assertIsInstance(response[0], UserGroup)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_group_by_id_returns_ok(self, mock_get):
        group_id = self.group_json.id
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.group)
        response = self.client.get_group(group_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, UserGroup)
        self.assertEqual(response.id, group_id)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_limit_returns_ok(self, mock_get):
        limit = 2
        # is it a valid test to manipulate the return data from a mocked function?
        filtered_groups = json.loads(self.groups)
        # just get the first 2 groups
        filtered_groups = filtered_groups[0:2]
        filtered_groups = json.dumps(filtered_groups)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(limit=limit)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], UserGroup)
        self.assertEqual(len(response), limit)
        self.assertGreater(len(response), 0)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_query_name_returns_ok(self, mock_get):
        query = "A Test Users"
        filtered_groups = json.loads("[{0}]".format(self.group))
        filtered_groups = json.dumps(filtered_groups)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(query=query)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], UserGroup)
        self.assertEqual(query, response[0].profile.name)
        self.assertGreater(len(response), 0)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_filter_by_id_returns_ok(self, mock_get):
        # filter supports a limited set of properties:
        # id, lastMembershipUpdated, lastUpdated, and type
        group_id = self.group_json.id
        filter_string = urllib.parse.quote_plus(
            "id eq \"{0}\"".format(group_id))
        filtered_groups = json.loads("[{0}]".format(self.group))
        filtered_groups = json.dumps(filtered_groups)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], UserGroup)
        self.assertEqual(response[0].id, group_id)
        self.assertGreater(len(response), 0)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_filter_by_lastMembershipUpdated_returns_ok(self, mock_get):
        filter_string = urllib.parse.quote_plus(
            "lastUpdated gt \"2019-12-17T00:00:00.000Z\"")
        filtered_groups = self.groups
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        # 5 users in the test data that are active
        self.assertEqual(len(response), 9)
        self.assertIsInstance(response[0], UserGroup)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_filter_by_lastUpdated_returns_ok(self, mock_get):
        filter_string = urllib.parse.quote_plus(
            "lastUpdated gt \"2019-12-17T00:00:00.000Z\"")
        filtered_groups = self.groups
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), 9)
        self.assertIsInstance(response[0], UserGroup)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_list_groups_with_filter_by_type_returns_ok(self, mock_get):
        group_type = "OKTA_GROUP"
        filter_string = urllib.parse.quote_plus(
            "type eq \"{0}\"".format(group_type))
        filtered_groups = json.loads("[{0}]".format(self.group))
        filtered_groups = json.dumps(filtered_groups)
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=filtered_groups)
        response = self.client.get_groups(filter_string=filter_string)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], UserGroup)
        self.assertEqual(response[0].type, group_type)
        self.assertGreater(len(response), 0)

    @patch("oktasdk.framework.ApiClient.requests.get")
    def test_get_group_users_returns_ok(self, mock_get):
        group_id = self.group_json.id
        mock_get.return_value = Mock(
            status_code=status.HTTP_200_OK, text=self.group_users)
        response = self.client.get_group_users(group_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0], User)
        self.assertEqual(len(response), 3)

    @skipIf(os.getenv("SKIP_REAL", True) == True, "Skipping tests that hit the real API server.")
    def test_group_data_model_matches_real_api(self):
        from dotenv import load_dotenv
        from os import path

        basedir = path.abspath(path.dirname(__file__))
        load_dotenv(path.join(basedir, ".env"))

        base_url = os.getenv("BASE_URL", None)
        api_token = os.getenv("API_TOKEN", None)

        # get a real user from a real Okta tenant
        real_client = UserGroupsClient(base_url=base_url, api_token=api_token)
        #actual = real_client.get_user("00upofwtwaGmrmIsm0h7")
        actual = real_client.get_groups(limit=1)[0]
        # take the object, serialize it to a string
        actual_str = json.dumps(actual, cls=Serializer, separators=(',', ':'))
        # then load is back as JSON so we can get the keys
        actual_json = json.loads(actual_str)

        # call the mock API
        with patch("oktasdk.framework.ApiClient.requests.get") as mock_get:
            mock_get.return_value = Mock(
                status_code=status.HTTP_200_OK, text=self.group)
            group_id = self.group_json.id
            mocked = self.client.get_group(group_id)
            mocked_str = json.dumps(
                mocked, cls=Serializer, separators=(',', ':'))
            mocked_json = json.loads(mocked_str)

        self.assertTrue(json_compare(actual_json, mocked_json))
