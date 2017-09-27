# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from contracts.models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dates', {'fields': ('start_date', 'end_date')}),
        ('Details', {
            'fields': ('property', 'tenant', 'rent'),
        }),
    )
    list_display = ('start_date', 'end_date', 'property',
                    'get_tenant_name', 'rent')
    list_filter = ('start_date', 'end_date')
    search_fields = ('tenant__first_name', 'tenant__last_name',
                     'property__street', 'property__city',
                     'property__zip_code')

    def get_tenant_name(self, obj):
        return obj.tenant.get_full_name()
    get_tenant_name.short_description = 'Tenant'
