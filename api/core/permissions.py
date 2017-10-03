# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Grants permissions for authenticated staff users"""

    def has_permission(self, request, view):
        return request.user.is_staff
