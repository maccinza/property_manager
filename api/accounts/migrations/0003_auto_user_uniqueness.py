# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 03:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_landlord_tenant'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set([('email', 'first_name', 'last_name')]),
        ),
    ]
