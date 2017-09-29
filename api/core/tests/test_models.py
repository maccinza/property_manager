# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

import string

from django.test import TestCase

from core.models import get_hash_id


class TestHashId(TestCase):
    valid_chars = set(string.ascii_letters + string.digits)

    def test_get_hash_id(self):
        """Should successfully get hash id with 16 valid chars"""
        hash_id = get_hash_id()
        self.assertEqual(len(hash_id), 16)
        for char in hash_id:
            self.assertIn(char, self.valid_chars)

    def test_get_custom_length_hash_id(self):
        """Should successfully get hash id with custom length valid chars"""
        hash_id = get_hash_id(hash_length=9)
        self.assertEqual(len(hash_id), 9)
        for char in hash_id:
            self.assertIn(char, self.valid_chars)
