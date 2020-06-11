import unittest
import os
import json

from flask_api import status
from unittest import skipIf
from unittest.mock import Mock, patch
from oktasdk.FactorsClient import FactorsClient
from oktasdk.framework.Utils import Utils
from oktasdk.framework.Serializer import Serializer
from oktasdk.models.factor.Factor import Factor


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

    def tearDown(self):
        pass

    @patch("okta.framework.ApiClient.requests.get")
    def test_get_factors(self, mock_get):
        # Configure the mock to return a response with an OK status code
        # and the raw text response (unparsed JSON)
        mock_get.return_value = Mock(status_code=200, text=self.factors)
        response = self.client.get_lifecycle_factors(self.user_id)
        factor_json = Utils.deserialize(self.factors, Factor)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, list)
        self.assertEqual(len(response), len(factor_json))
        self.assertIsInstance(response[0], Factor)

    @patch("okta.framework.ApiClient.requests.get")
    def test_get_factor_by_id(self, mock_get):
        mock_get.return_value = Mock(status_code=200, text=self.factor)
        response = self.client.get_factor(self.user_id, self.factor_id)

        self.assertIsNotNone(response)
        self.assertIsInstance(response, Factor)
        self.assertEqual(response.id, self.factor_id)
