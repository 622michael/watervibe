from __future__ import unicode_literals

from django.db import models

# Right now this app has a dependency on the FitBit app
# Reminder model should eventually include refrence to an abstract user class
# That is not reliant on the specific fitbit.user class

class User(models.Model):
	app = models.CharField(max_length=256)
	app_id = models.IntegerField(default = 0)

	start_of_period = models.CharField(max_length=22, null = True)
	end_of_period = models.CharField(max_length=22, null= True)
	next_sync_time = models.CharField(max_length=22, null = True)

	ounces_in_a_day = models.FloatField(default = 64.0, null = True)
	drink_size = models.FloatField(default = 8.0)

	maximum_reminders = models.IntegerField(default=8)

	last_update = models.CharField(max_length=22, null = True)
	last_sync = models.CharField(max_length=22, null = True)

	beginning_sample_date = models.CharField(max_length = 22, null = True)


class Reminder(models.Model):
	time = models.CharField(max_length = 22)
	user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	app = models.CharField(max_length = 256, default = "fitbit")
	app_id = models.IntegerField(null = True)


class Time (models.Model):
	minute = models.IntegerField()
	hour = models.IntegerField()

class Event (models.Model): 
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	tag = models.CharField(max_length = 256)
	start_time = models.FloatField(default = 0.0)
	end_time = models.FloatField(default = 0.0)
	day_of_week = models.IntegerField(default = 0)
	probability = models.FloatField(null = True)
	probability_variance = models.FloatField(null = True)
	fringe_probability = models.FloatField(null = True)
	fringe_variance = models.FloatField(null = True)

	start_date = models.CharField(max_length = 22)
	end_date = models.CharField(max_length = 22)
	times = models.ManyToManyField(Time)