# -*- encoding: UTF-8 -*-
from dev import * # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'property_management.sqlite',
    }
}
