# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter(trailing_slash=False)


urlpatterns = [
    url(r'^', include(router.urls)),

]
