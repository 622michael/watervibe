from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class User(models.Model):
	fitbit_id = models.CharField(max_length = 25)
	access_token = models.CharField(max_length = 260)
	scope= models.CharField(max_length = 260)
	refresh_token= models.CharField(max_length = 64)
	access_token_expiration = models.CharField(max_length = 22, default="2090-09-15 12:00+00:00")
	
	# Profile fields
	weight = models.FloatField(default = 0.0)


class Device(models.Model):
	fitbit_id = models.CharField(max_length = 20)
	version = models.CharField(max_length = 260)
	device_type = models.CharField(max_length = 260)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

class Alarm(models.Model):
	fitbit_id = models.CharField(max_length = 15)
	time = models.CharField(max_length = 22) 
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	device = models.ForeignKey(Device, on_delete = models.CASCADE)
