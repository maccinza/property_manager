# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

import factory

from properties.models import Property
from accounts.tests.factories import LandlordFactory


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Property

    street = factory.Iterator(["Baker Street", "Second Street"])
    number = factory.Iterator(["100", "200"])
    zip_code = factory.Iterator(["NW16XE", "NW89XZ"])
    city = factory.Iterator(["London", "South Yorkshire"])
    description = factory.Iterator(
        ["Amazing location", "Fantastic rent price"])
    category = factory.Iterator(["apartment", "flat"])
    beds = factory.Iterator(["2", "1"])
    landlord = factory.SubFactory(LandlordFactory)
