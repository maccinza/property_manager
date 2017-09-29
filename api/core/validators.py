# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

import string

from django.core.exceptions import ValidationError


def validate_hash_id(value):
    """
    Raises a ValidationError if hash id has not length 16 or contains invalid
    characters
    """
    valid_chars = set(string.ascii_lowercase + string.digits)
    if not set(value).issubset(valid_chars) or len(value) != 16:
        raise ValidationError('ID must be a string containing 16 '
                              'alphanumeric lowercase characters')
