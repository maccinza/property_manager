# -*- encoding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from accounts.serializers import TenantSerializer
from properties.serializers import PropertySerializer
from contracts.models import Contract


class ContractSerializer(serializers.HyperlinkedModelSerializer):
    tenant = TenantSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    created = serializers.SerializerMethodField()

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    class Meta:
        model = Contract
        fields = (
            'id', 'created', 'start_date', 'end_date', 'rent', 'property',
            'tenant')


class ContractModificationsSerializer(serializers.HyperlinkedModelSerializer):
    tenant = serializers.PrimaryKeyRelatedField(read_only=True)
    property = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.SerializerMethodField()

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')

    class Meta:
        model = Contract
        fields = (
            'id', 'created', 'start_date', 'end_date', 'rent', 'property',
            'tenant')
