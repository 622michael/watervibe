from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	fitbit_id = models.CharField(max_length=4)
	access_token = models.CharField(max_length=260)
	scope= models.CharField(max_length=260)
	refresh_token= models.CharField(max_length=64)
