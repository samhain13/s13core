# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-23 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content_management', '0007_auto_20180320_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileasset',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
