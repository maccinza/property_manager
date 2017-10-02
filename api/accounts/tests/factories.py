# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from accounts.models import Landlord, Tenant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Iterator(["Elon", "Jeff"])
    last_name = factory.Iterator(["Musk", "Bezos"])
    username = factory.LazyAttribute(
        lambda obj: "{}_{}".format(
            obj.first_name.lower(), obj.last_name.lower()))
    email = factory.LazyAttribute(
        lambda obj: "{}@email.com".format(obj.first_name.lower()))
    is_active = True
    is_staff = factory.Iterator([True, False])
    is_superuser = factory.Iterator([True, False])

    @factory.lazy_attribute
    def password(self):
        return make_password('password123!')


class LandlordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Landlord

    first_name = factory.Iterator(["George", "Ronda"])
    last_name = factory.Iterator(["Foreman", "Rousey"])
    email = factory.LazyAttribute(
        lambda obj: "{}@email.com".format(obj.first_name.lower()))


class TenantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tenant

    first_name = factory.Iterator(["Bill", "Nicole"])
    last_name = factory.Iterator(["Murray", "Kidman"])
    email = factory.LazyAttribute(
        lambda obj: "{}@email.com".format(obj.first_name.lower()))
