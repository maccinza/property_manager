# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string
import random

from django.db import models

from core.validators import validate_hash_id


def get_hash_id(hash_length=16):
    """
    Generates random 16 char lowercase string with numbers and
    lowercase letters
    """
    hash_seed = string.ascii_lowercase + string.digits
    hash_string = ''
    for x in random.sample(hash_seed, hash_length):
        hash_string += x
    return hash_string


class HashIdModel(models.Model):
    id = models.CharField(
        primary_key=True, max_length=16, default=get_hash_id,
        validators=[validate_hash_id], editable=False)

    class Meta:
        abstract = True


class PropertyBaseUser(HashIdModel):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super(PropertyBaseUser, self).save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        abstract = True
