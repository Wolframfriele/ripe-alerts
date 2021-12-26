from django.test import TestCase
from unittest.mock import Mock, patch
from ripe_atlas.interfaces import RipeInterface

"""Integration tests Ripe Atlas"""


class FirstTest(TestCase):

    def test_hello_world(self):
        text = "hello world!"
        self.assertEqual(text, "hello world!")


class TestRipeInterface(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_response_patcher = patch('ripe_atlas.interfaces.requests.get')
        cls.mock_response = cls.mock_response_patcher.start()
        cls.valid_token = "115c25fc-8815-4710-9865-85d49dc4778a"
        cls.invalid_token = ""

    @classmethod
    def tearDownClass(cls):
        cls.mock_response_patcher.stop()

    """
    When we send a request to Ripe Atlas and we use a ripe_api_token, when the token is invalid we
    get a 403 status code and if token is valid we get a 200 status code
    """

    def test_is_token_valid_when_valid(self):
        self.mock_response.return_value.status_code = 200
        valid = RipeInterface.is_token_valid(self.valid_token)
        self.assertTrue(valid)

    def test_is_token_valid_when_invalid(self):
        self.mock_response.return_value.status_code = 403
        invalid = RipeInterface.is_token_valid(self.invalid_token)
        self.assertFalse(invalid)

