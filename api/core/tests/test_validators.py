# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.exceptions import ValidationError

from core.models import get_hash_id
from core.validators import validate_hash_id


class TestHashIdValidation(TestCase):
    def test_successfully_validate_hash_id(self):
        """
        Should successfully validate given hash id when it obeys
        requirements
        """
        hash_id = get_hash_id()
        self.assertIsNone(validate_hash_id(hash_id))

    def test_fail_validating_hash_id_length(self):
        """
        Should raise ValidationError when trying to validate hash id
        with invalid length
        """
        hash_id = get_hash_id(hash_length=8)
        expected = ('ID must be a string containing 16 '
                    'alphanumeric lowercase characters')
        with self.assertRaises(ValidationError) as raised:
            validate_hash_id(hash_id)
        self.assertEqual(raised.exception.message, expected)

    def test_fail_validating_hash_id_chars(self):
        """
        Should raise ValidationError when trying to validate hash id with
        invalid characters
        """
        hash_id = 'aaaa&bbbb#cccc**'
        expected = ('ID must be a string containing 16 '
                    'alphanumeric lowercase characters')
        with self.assertRaises(ValidationError) as raised:
            validate_hash_id(hash_id)
        self.assertEqual(raised.exception.message, expected)
