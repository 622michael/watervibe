from django.core.management.base import BaseCommand, CommandError
from watervibe import users
from watervibe.watervibe_time import string_for_day
import importlib

class Command(BaseCommand):
	def handle(self, *args, **options):

		##	Calculate weighted average
		##  time waken up, and the accuracy
		##  this would hold if used as a measure
		##  for when to set an alarm.
		for user in users.users():
			print "------ BEGIN SLEEP INFO %d ---------" % user.id
			for day_of_the_week in range(1,7):
				average = users.weighted_average_wake_time(user, 
												 day_of_the_week)

				success = 0
				total = 0
				app = importlib.import_module(user.app + "." + user.app)
				wake_times = app.wake_times(user)

				for wake_time in wake_times:
					wake_time_date = watervibe.date_for_string(wake_time)
					if wake_time_date.isoweekday() == day_of_the_week:
						if average > wake_time:
							success += 1
						total += 1
	
				if total != 0:
					accuracy = success/total
				else: 
					accuracy = 0

				day = string_for_day(day_of_the_week)

				print "%s: %f %.2f" % (day, average, accuracy*100)


			print "------ END SLEEP INFO %d ---------" % user.id


