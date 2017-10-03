# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from accounts.serializers import LandlordSerializer
from properties.models import Property


class PropertySerializer(serializers.HyperlinkedModelSerializer):
    landlord = LandlordSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'city', 'zip_code', 'street', 'number', 'description',
                  'category', 'beds', 'landlord')


class PropertyModificationsSerializer(serializers.HyperlinkedModelSerializer):
    landlord = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Property
        fields = ('id', 'city', 'zip_code', 'street', 'number', 'description',
                  'category', 'beds', 'landlord')
