from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.
class User(models.Model):
	fitbit_id = models.CharField(max_length = 4)
	access_token = models.CharField(max_length = 260)
	scope= models.CharField(max_length = 260)
	refresh_token= models.CharField(max_length = 64)

	# The following data is not relavent to fitbit
	# For portability, this information should be stored
	# In another model. fitbit and watervibe should not
	# Depend upon once another.
	start_of_period = models.DateTimeField(null = True)
	end_of_period = models.DateTimeField(null= True)
	ounces_in_a_period = models.FloatField(default = 64.0, null = True)
	drink_size = models.FloatField(default = 8.0)


class Device(models.Model):
	fitbit_id = models.CharField(max_length = 8)
	version = models.CharField(max_length = 260)
	device_type = models.CharField(max_length = 260)
	user = models.ForeignKey(User, on_delete = models.CASCADE)

class Alarm(models.Model):
	fitbit_id = models.CharField(max_length = 8)
	time = models.CharField(max_length = 11) 
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	device = models.ForeignKey(Device, on_delete = models.CASCADE)
