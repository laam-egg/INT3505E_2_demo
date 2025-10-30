import unittest

from flask import json

from openapi_server.models.user import User  # noqa: E501
from openapi_server.models.user_create import UserCreate  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_users_get(self):
        """Test case for users_get

        List all users
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/v1/users',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_post(self):
        """Test case for users_post

        Create a new user
        """
        user_create = {"password":"password","name":"name","email":"email"}
        headers = { 
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/api/v1/users',
            method='POST',
            headers=headers,
            data=json.dumps(user_create),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
