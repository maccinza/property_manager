# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from core.models import PropertyBaseUser


class Landlord(PropertyBaseUser):
    """Landlord user representation"""
    pass


class Tenant(PropertyBaseUser):
    """Tenant user representation"""
    pass
