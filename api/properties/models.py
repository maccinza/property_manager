# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from accounts.models import Landlord


class Property(models.Model):
    """Property representation"""

    CATEGORY_CHOICES = (
        ('house', 'House'),
        ('apartment', 'Apartment'),
        ('flat', 'Flat'),
        ('other', 'Other'))

    BED_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4+', '4+'))

    street = models.CharField(
        max_length=150, help_text=u'street where property is located')

    number = models.CharField(
        max_length=10, help_text=u'property number on the street')

    zip_code = models.CharField(
        max_length=15, help_text=u'zip code of the property')

    city = models.CharField(
        max_length=100, help_text=u'city where property is located')

    description = models.TextField(
        max_length=2000, help_text=u'general description of property')

    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES,
        help_text=u'most adequate category for property',
        default=CATEGORY_CHOICES[0][0],)

    beds = models.CharField(
        max_length=2, choices=BED_CHOICES,
        help_text=u'number of bedrooms in the property',
        default=BED_CHOICES[0][0])

    landlord = models.ForeignKey(Landlord, help_text=u'owner of the property',
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Property, self).save(*args, **kwargs)

    def clean(self):
        self.zip_code = self.zip_code.replace(' ', '')

    def __unicode__(self):
        return u'{} at {}, {} - {}'.format(
            self.get_category_display(), self.street, self.number, self.city)
