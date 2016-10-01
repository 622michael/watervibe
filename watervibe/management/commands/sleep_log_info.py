from django.core.management.base import BaseCommand, CommandError
from watervibe import users
from watervibe import stats
from watervibe.watervibe_time import string_for_day, date_for_string
from watervibe.models import Time
import importlib

class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in users.users():
			## Calculate probability for all times
			print "------ BEGIN PMD: %d ---------" % user.id
			for time in Time.objects.all():
				probability = stats.probability("sleep", time, user = user)

				print "%d:%d -> %.2f" % (time.hour, time.minute, probability*100)

			print "------ END PMD: %d ---------" % user.id
			
			## Calculate probablity asleep for all times on a specific day
			
			for day_of_week in range(1,8):
				print "------ BEGIN %s PMD: %d ---------" % (string_for_day(day_of_week), user.id)
				for time in Time.objects.all():
					probability = stats.probability("sleep", time, user = user, day_of_week = day_of_week)
					
					print "%d:%d -> %.2f" % (time.hour, time.minute, probability*100)
				print "------ END %s PMD: %d ---------" % (string_for_day(day_of_week), user.id)	

			##	Calculate weighted average
			##  time waken up, and the accuracy
			##  this would hold if used as a measure
			##  for when to set an alarm.

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
				sleep_times, wake_times = app.sleep_times(user.id)

				day_wake_times = []
				day_sleep_times = []
				for x in range(0, len(wake_times)):
					wake_time = wake_times[x]
					sleep_time = sleep_times[x]

					wake_time_date = date_for_string(wake_time)
					sleep_time_date = date_for_string(sleep_time)

					start_of_period = wake_time_date.replace(hour = int(wake_average), minute = int((wake_average % 1)*60))
					end_of_period = sleep_time_date.replace(hour = int(sleep_average), minute = int((sleep_average % 1)*60))
						
					if wake_time_date.isoweekday() is day_of_the_week:
						day_wake_times.append(wake_time)
						day_sleep_times.append(sleep_time)
						
						if start_of_period > wake_time_date:
							wake_success += 1
						if end_of_period < sleep_time_date:
							sleep_success += 1
						if end_of_period < sleep_time_date and start_of_period > wake_time_date:
							success += 1
						total += 1
	
				if total != 0:
					wake_accuracy = wake_success/total
					sleep_accuracy = sleep_success/total
					accuracy = success/total
				else: 
					accuracy = 0

				day = string_for_day(day_of_the_week)

				print "%s: (%f - %f) %.2f" % (day, sleep_average, wake_average, accuracy*100)
				print "\t Starting Period Accuracy: %.2f" % wake_accuracy
				print "\t Ending Period Accuracy: %.2f" % sleep_accuracy
				print "\t \t Sleep times: %s" % day_sleep_times
				print "\t \t Wake times: %s" % day_wake_times


			print "------ END SLEEP INFO %d ---------" % user.id


