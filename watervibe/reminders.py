### Watervibe reminders:
## Handles the reminders 
## 
##
##

import users
from watervibe_time import date_for_string
from models import Reminder

def create_reminder(time, user):
	Reminder.objects.create(time= string_for_date(time, offset=users.user_timezone(user)),
							user= user)

def create_reminders_for_user(user):
	available_reminders = reminders_available_at_next_sync(user)
	start_of_period, end_of_period = users.period_for_user(user)

	for x in range(0, available_reminders):
		last_reminder = last_reminder_for_user(user)
		next_reminder_time = date_for_string(last_reminder.time) + time_between_reminders_for_user(user)

		if start_of_period < next_reminder_time < end_of_period: 
			next_reminder_time = start_of_period

		create_reminder(next_reminder_time, user)