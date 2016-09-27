from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import users, reminders
from watervibe.watervibe_time import now_in_user_timezone
import importlib
from datetime import timedelta

##	Add Reminders
##  --------------------------------------
##	This task is responisbile for adding 
##  reminders for all users until the
##  next sync time has all of its spots full
class Command(BaseCommand):
	def handle(self, *args, **options):
		all_users = User.objects.all().order_by('next_sync_time')

		for user in all_users:
			user_reminders = users.user_reminders(user)

			num_reminders = len(users.reminders_at_next_sync(user))
			max_reminders = users.maximum_reminders(user)
			
			while num_reminders < max_reminders:
				print "Num reminders: %s" % num_reminders
				print "Max reminders: %s" % max_reminders

				now = now_in_user_timezone
				start_of_period, end_of_period = users.period_for_user(user)

				## Initalize the first reminder if there isn't any
				## Start at the beginning of the period and add the
				## Maximum time between reminders till it is past the present
				if user_reminders.first() is None:
					next_reminder_time = start_of_period
					next_reminder_date = now.replace(hour = next_reminder_time.hour,
													 minute = next_reminder_time.minute)

					while next_reminder_date < now:
						next_reminder_date = next_reminder_date + users.maximum_time_between_reminders(user)

						if next_reminder_date.hour > end_of_period.hour:
							next_reminder_date += timedelta(days = 1)
							next_reminder_date = next_reminder_date.replace(hour = start_of_period.hour,
													 						minute  = start_of_period.minute)
				else:
					last_reminder = user_rwateminders.last()
					next_reminder_date = reminders.date(last_reminder) + users.maximum_time_between_reminders(user)
					if next_reminder_date.hour > end_of_period.hour:
						next_reminder_date += timedelta(days = 1)
						next_reminder_date = next_reminder_date.replace(hour = start_of_period.hour,
												 						minute  = start_of_period.minute)

				reminders.create_reminder(next_reminder_date, user)
				num_reminders = len(users.reminders_at_next_sync(user))
				
