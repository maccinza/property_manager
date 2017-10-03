# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from properties.models import Property


def is_category_valid(category):
    """Checks if a given category of properties is valid"""
    valid_categories = [cat[0].lower() for cat in Property.CATEGORY_CHOICES]
    return category.lower() in valid_categories


def is_number_of_beds_valid(num_beds):
    """Checks if a given quantity of beds of a property is valid"""
    valid_beds = [bed[0] for bed in Property.BED_CHOICES]
    return num_beds in valid_beds
