# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 14:25
from __future__ import unicode_literals

import core.models
import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.CharField(default=core.models.get_hash_id, editable=False, max_length=16, primary_key=True, serialize=False, validators=[core.validators.validate_hash_id]),
        ),
    ]
