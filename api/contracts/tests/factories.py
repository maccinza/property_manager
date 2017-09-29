# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

import factory

from contracts.models import Contract
from accounts.tests.factories import TenantFactory
from properties.tests.factories import PropertyFactory


class ContractFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contract

    start_date = factory.Iterator(['2017-09-25', '2017-10-22'])
    end_date = factory.Iterator(['2018-09-25', '2018-09-22'])
    property = factory.SubFactory(PropertyFactory)
    tenant = factory.SubFactory(TenantFactory)
    rent = factory.Iterator([1250.25, 875.00])
