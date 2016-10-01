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
			for day_of_the_week in range(1,8):
				wake_average = users.weighted_average_wake_time(user, 
												 day_of_the_week)
				sleep_average = users.weighted_average_sleep_time(user,
											day_of_the_week)

				# Testing: A success case is when the period specified
				# by wake_average and wake_sleep do not let an alarm be
				# set at a time during a sleeping time.
				wake_success = 0
				sleep_success = 0
				success = 0
				total = 0
				app = importlib.import_module(user.app + "." + user.app)
				sleep_times, wake_times = app.sleep_times(user)

				for x in range(0, len(wake_times)):
					wake_time = wake_times[i]
					sleep_time = sleep_times[i]

					wake_time_date = watervibe.date_for_string(wake_time)
					sleep_time_date = watervibe.date_for_string(sleep_time)

					start_of_period = wake_time_date.replace(hour = int(wake_average), minute = wake_average % 1)
					end_of_period = sleep_time_date.replace(hour = int(sleep_average), minute = sleep_average % 1)

					if wake_time_date.isoweekday() == day_of_the_week:
						if start_of_period > wake_time:
							wake_success += 1
						if end_of_period < sleep_time:
							sleep_success += 1
						if end_of_period < sleep_time and start_of_period > wake_time:
							success += 1
						total += 1
	
				if total != 0:
					wake_accuracy = wake_success/total
					sleep_accuracy = sleep_success/total
					accuracy = success/total
				else: 
					accuracy = 0

				day = string_for_day(day_of_the_week)

				print "%s: %f %.2f" % (day, average, accuracy*100)
				print "\t Starting Period Accuracy: %.2f" % wake_accuracy
				print "\t Ending Period Accuracy: %.2f" % sleep_accuracy


			print "------ END SLEEP INFO %d ---------" % user.id


