# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('properties', '0001_initial'),
        ('accounts', '0003_auto_user_uniqueness'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='contract creation date and time')),
                ('start_date', models.DateField(help_text='starting date for the contract')),
                ('end_date', models.DateField(help_text='ending date for the contract')),
                ('rent', models.DecimalField(decimal_places=2, help_text='monthly value in pounds that should be payed by tenant', max_digits=10)),
                ('property', models.ForeignKey(help_text='property associated with the contract', on_delete=django.db.models.deletion.CASCADE, to='properties.Property')),
                ('tenant', models.ForeignKey(help_text='tenant associated with the contract', on_delete=django.db.models.deletion.CASCADE, to='accounts.Tenant')),
            ],
        ),
    ]
