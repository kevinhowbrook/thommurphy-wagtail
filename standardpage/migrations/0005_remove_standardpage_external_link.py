# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-22 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standardpage', '0004_standardpage_external_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standardpage',
            name='external_link',
        ),
    ]
