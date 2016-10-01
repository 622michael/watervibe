from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class User(models.Model):
	fitbit_id = models.CharField(max_length = 25)
	access_token = models.CharField(max_length = 260)
	scope= models.CharField(max_length = 260)
	refresh_token= models.CharField(max_length = 64)
	access_token_expiration = models.CharField(max_length = 22, default="2012-09-15 12:00+00:00")
	
	last_sleep_sync = models.CharField(max_length = 22, null = True)

	# Profile fields
	weight = models.FloatField(default = 0.0)
	timezone = models.CharField(max_length = 260, null = True)

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


class Sleep(models.Model):
	fitbit_id = models.CharField(max_length = 20)
	is_main_sleep = models.IntegerField()
	start_time = models.CharField(max_length = 22)
	end_time = models.CharField(max_length = 22)
	duration = models.IntegerField()
	user = models.ForeignKey(User, on_delete = models.CASCADE)
