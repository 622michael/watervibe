# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-18 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitbit', '0007_auto_20160918_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fitbit_id',
            field=models.CharField(max_length=25),
        ),
    ]