# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts.views import LandlordView, TenantView
from properties.views import PropertyView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'landlords', LandlordView, base_name='landlords')
router.register(r'tenants', TenantView, base_name='tenants')
router.register(r'properties', PropertyView, base_name='properties')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/login$', obtain_jwt_token),
    url(r'^auth/refresh-token$', refresh_jwt_token),
]
