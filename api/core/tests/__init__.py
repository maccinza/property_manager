from __future__ import unicode_literals

from rest_framework.test import APITestCase


class JWTAuthenticationTestCase(APITestCase):

    def get_jwt_header(self, email, password):
        payload = {
            "email": email,
            "password": password
        }
        response = self.client.post("/api/auth/login", data=payload)
        token = response.data['token']
        headers = {
            "HTTP_AUTHORIZATION": "JWT {}".format(token)
        }
        return headers
