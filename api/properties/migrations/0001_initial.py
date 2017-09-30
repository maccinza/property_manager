# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-30 03:08
from __future__ import unicode_literals

import core.models
import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.CharField(default=core.models.get_hash_id, editable=False, max_length=16, primary_key=True, serialize=False, validators=[core.validators.validate_hash_id])),
                ('street', models.CharField(help_text='street where property is located', max_length=150)),
                ('number', models.CharField(help_text='property number on the street', max_length=10)),
                ('zip_code', models.CharField(help_text='zip code of the property', max_length=15)),
                ('city', models.CharField(help_text='city where property is located', max_length=100)),
                ('description', models.TextField(help_text='general description of property', max_length=2000)),
                ('category', models.CharField(choices=[('house', 'House'), ('apartment', 'Apartment'), ('flat', 'Flat'), ('other', 'Other')], default='house', help_text='most adequate category for property', max_length=10)),
                ('beds', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4+', '4+')], default='1', help_text='number of bedrooms in the property', max_length=2)),
                ('landlord', models.ForeignKey(help_text='owner of the property', on_delete=django.db.models.deletion.CASCADE, to='accounts.Landlord')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
    ]
