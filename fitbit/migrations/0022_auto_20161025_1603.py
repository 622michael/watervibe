# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-25 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbit', '0021_auto_20161025_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=260, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(max_length=260, null=True),
        ),
    ]
