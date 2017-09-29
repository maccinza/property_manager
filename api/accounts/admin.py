# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (AdminPasswordChangeForm, UserChangeForm,
                                       UserCreationForm)

from accounts.models import User, Landlord, Tenant


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                         'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


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
