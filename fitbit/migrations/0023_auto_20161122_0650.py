# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-22 06:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbit', '0022_auto_20161025_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(default='', max_length=260, null=True),
        ),
    ]