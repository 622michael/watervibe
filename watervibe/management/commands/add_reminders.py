from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import users, reminders
from watervibe.watervibe_time import now_in_user_timezone
import importlib

##	This task is responsible for adding reminders
## 	For all users untill the sync after next has the
##	Maximum number of reminders for their app.
class Command(BaseCommand):
	def handle(self, *args, **options):
		all_users = User.objects.all().order_by('next_sync_time')

		for user in all_users:
			user_reminders = users.user_reminders(user)

			num_reminders = users.reminders_at_next_sync(user).count
			max_reminders = users.maximum_reminders(user)

			while num_reminders < max_reminders:
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
					last_reminder = user_reminders.last()
					next_reminder_date = reminders.date(last_reminder) + users.maximum_time_between_reminders(user)
					if next_reminder_date.hour > end_of_period.hour:
						next_reminder_date += timedelta(days = 1)
						next_reminder_date = next_reminder_date.replace(hour = start_of_period.hour,
												 						minute  = start_of_period.minute)

				reminders.create_reminder(user, next_reminder_date)
				num_reminders = users.reminders_at_next_sync(user).count()
				