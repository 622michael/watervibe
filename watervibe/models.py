from __future__ import unicode_literals

from django.db import models

# Create your models here.

# Right now this app has a dependency on the FitBit app
# Reminder model should eventually include refrence to an abstract user class
# That is not reliant on the specific fitbit.user class


class Reminder(models.Model):
	time = models.DateField()
