import json
import logging
from datetime import datetime

from django.test import TestCase
from django.urls import reverse

from .views import decode_token, encode_token

STATUS_CRED_ERROR = 403
STATUS_CRED_SUCCESS = 200

logging.disable(logging.CRITICAL)


class AuthJWTTestCase(TestCase):
    """
    Basic tests for authenticating users with jwt
    """

    def setUp(self):
        self.endpoint = "jwt_auth"

    def test_decode_encode(self):
        user_id = 1
        encoded_payload = encode_token(user_id, datetime.utcnow())
        decoded_payload = decode_token(encoded_payload)
        expected_decoded = {'user_id': user_id}
        self.assertEquals(expected_decoded, decoded_payload)

    def test_incorrectly_signed_token_not_accepted_code(self):
        response = self.client.post(reverse(self.endpoint),
                                    {'token': 'testtest'})
        self.assertEquals(response.status_code, STATUS_CRED_ERROR)

    def test_incorrectly_signed_token_not_accepted_code_msg(self):
        response = self.client.post(reverse(self.endpoint),
                                    {'token': 'testtest'})
        error_msg = json.loads(response.content.decode("UTF-8"))
        self.assertIn("Error", error_msg.keys())

    def test_token_doesnt_exist_errors_code(self):
        response = self.client.post(reverse(self.endpoint),
                                    {"token_false": "testtest"})
        self.assertEquals(response.status_code, STATUS_CRED_ERROR)

    def test_token_doesnt_exist_errors_msg(self):
        response = self.client.post(reverse(self.endpoint),
                                    {"token_false": "testtest"})
        error_msg = json.loads(response.content.decode("UTF-8"))
        self.assertIn("Error", error_msg.keys())

    def create_valid_token(self, user_id, exp):
        encoded_payload = encode_token(user_id, exp)
        response = self.client.post(reverse(self.endpoint),
                                    {"token": encoded_payload})
        return response

    def test_correct_token_validates_correctly_code(self):
        user_id = 1
        response = self.create_valid_token(user_id, datetime.utcnow())
        self.assertEquals(response.status_code, STATUS_CRED_SUCCESS)

    def test_correct_token_validates_correctly_msg(self):
        user_id = 1
        response = self.create_valid_token(user_id, datetime.utcnow())
        success_msg = json.loads(response.content.decode("UTF-8"))
        self.assertIn("Status", success_msg.keys())

    def test_correct_token_returns_correct_user_id(self):
        user_id = 1
        response = self.create_valid_token(user_id, datetime.utcnow())
        res_header_user = int(response['x-maximus-user'])
        self.assertEquals(user_id, res_header_user)
