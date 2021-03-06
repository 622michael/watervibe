# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 18:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitbit_id', models.CharField(max_length=8)),
                ('time', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitbit_id', models.CharField(max_length=8)),
                ('version', models.CharField(max_length=260)),
                ('device_type', models.CharField(max_length=260)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitbit_id', models.CharField(max_length=4)),
                ('access_token', models.CharField(max_length=260)),
                ('scope', models.CharField(max_length=260)),
                ('refresh_token', models.CharField(max_length=64)),
                ('start_of_period', models.DateTimeField(null=True)),
                ('end_of_period', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitbit.User'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitbit.Device'),
        ),
        migrations.AddField(
            model_name='alarm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitbit.User'),
        ),
    ]
