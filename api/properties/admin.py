# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from properties.models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('landlord',)}),
        ('Property characteristics', {
            'fields': ('category', 'beds', 'description'),
        }),
        ('Property location', {
            'fields': ('city', 'street', 'number', 'zip_code'),
        }),
    )
    list_display = ('get_landlord_name', 'category', 'beds', 'city', 'street',
                    'number', 'zip_code')
    list_filter = ('beds', 'category')
    search_fields = ('landlord__first_name', 'landlord__first_name',
                     'description', 'city', 'street', 'zip_code')
    ordering = ('id',)

    def get_landlord_name(self, obj):
        return obj.landlord.get_full_name()
    get_landlord_name.short_description = 'Landlord'
