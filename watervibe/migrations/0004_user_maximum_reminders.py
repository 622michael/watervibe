# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watervibe', '0003_user_next_sync_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='maximum_reminders',
            field=models.IntegerField(default=8),
        ),
    ]
