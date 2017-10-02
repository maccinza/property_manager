# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from accounts.models import Landlord, Tenant


class PropertyUserSerializer(serializers.HyperlinkedModelSerializer):

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.get_full_name()


class LandlordSerializer(PropertyUserSerializer):

    class Meta:
        model = Landlord
        fields = ('id', 'name', 'email')


class LandlordModificationSerializer(PropertyUserSerializer):

    class Meta:
        model = Landlord
        fields = ('id', 'first_name', 'last_name', 'email')


class TenantSerializer(PropertyUserSerializer):

    class Meta:
        model = Tenant
        fields = ('id', 'name', 'email')


class TenantModificationSerializer(PropertyUserSerializer):

    class Meta:
        model = Tenant
        fields = ('id', 'first_name', 'last_name', 'email')
