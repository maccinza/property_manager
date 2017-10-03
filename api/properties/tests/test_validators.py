# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from properties.validators import is_category_valid, is_number_of_beds_valid


class TestCategoryValidator(TestCase):
    def test_category_is_valid(self):
        """Should return True when given category is valid"""
        categories = ['house', 'HOUSE', 'apartment', 'Apartment',
                      'flat', 'FLAT', 'Other', 'other']
        self.assertTrue(all(is_category_valid(cat) for cat in categories))

    def test_category_is_invalid(self):
        """Should return False when given category is invalid"""
        categories = ['studio', 'invalid', 'minka']
        for cat in categories:
            self.assertFalse(is_category_valid(cat))


class TestValidBeds(TestCase):
    def test_bed_is_valid(self):
        """Should return True when given bed number is valid"""
        beds = ['1', '2', '3', '4+']
        self.assertTrue(all(is_number_of_beds_valid(bed) for bed in beds))

    def test_bed_is_invalid(self):
        """Should return False when given bed number is invalid"""
        beds = ['5', '0', '6+', '10']
        for bed in beds:
            self.assertFalse(is_number_of_beds_valid(bed))
