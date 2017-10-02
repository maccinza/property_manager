# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions

from django.contrib.auth.models import User


class IsAdminUser(permissions.BasePermission):
    """Grants permissions for authenticated staff users"""

    def has_permission(self, request, view):
        return request.user.is_staff
