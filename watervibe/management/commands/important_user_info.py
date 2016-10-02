from django.core.management.base import BaseCommand, CommandError
from watervibe import users
from watervibe.watervibe_time import now_in_user_timezone
from datetime import timedelta

## This command returns info about users
## When will WaterVibe determine they are asleep in the coming day?
## What is the maximum time between reminders?
## How many ounces are setup for the current period?
 
class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in users.users():
			start_of_period = now_in_user_timezone(user)
			end_of_period = start_of_period + timedelta(days = 1)
			ounces_drunk_in_period = users.ounces_to_drink_in_period(user, start_of_period, end_of_period)
			time_between_reminders = users.maximum_time_between_reminders(user, start_of_period)

			print "%d: %d %d" % (user.id, ounces_drunk_in_period, time_between_reminders.total_seconds())
		
