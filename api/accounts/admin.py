# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from accounts.models import Landlord, Tenant


class BasePropertyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    fieldsets = (
        ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(Landlord)
class LandlordAdmin(BasePropertyUserAdmin):
    pass


@admin.register(Tenant)
class TenantAdmin(BasePropertyUserAdmin):
    pass
