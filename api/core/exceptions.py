# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework.exceptions import APIException
from rest_framework import status


class Api401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Action not allowed'

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail
