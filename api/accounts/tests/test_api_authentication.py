# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

import json

from rest_framework.test import APITestCase
from rest_framework import status

from accounts.tests.factories import UserFactory


class TestAPIAuthentication(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_token_for_valid_credentials(self):
        """
        Should successfully get authorization token for valid given
        credentials
        """
        payload = {
            'username': self.user.username,
            'password': 'password123!'
        }
        response = self.client.post('/api/auth/login', data=payload)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', data)
        self.assertTrue(data['token'])

    def test_fail_to_get_token_invalid_credentials(self):
        """
        Should fail getting authorization token for invalid given credentials
        """
        payload = {
            'username': self.user.username,
            'password': 'wrongpwdforuser'
        }
        response = self.client.post('/api/auth/login', data=payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = json.loads(response.content)
        expected = {
            'non_field_errors': [
                'Unable to log in with provided credentials.'
            ]
        }
        self.assertEqual(data, expected)

    def test_refresh_token_for_valid_credentials(self):
        """
        Should successfully refresh authorization token for valid given
        credentials
        """
        payload = {
            'username': self.user.username,
            'password': 'password123!'
        }
        # gets auth token
        response = self.client.post('/api/auth/login', data=payload)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', data)
        token = data['token']
        self.assertTrue(token)

        payload['token'] = token
        # refresh token
        response = self.client.post('/api/auth/refresh-token', data=payload)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', data)
