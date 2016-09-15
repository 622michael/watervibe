### Watervibe reminders:
## Handles the reminders 
## 
##
##

import users
import watervibe_time
# from watervibe_time import date_for_string, string_for_datepyth
from models import Reminder
from datetime import timedelta

def reminders_available_at_next_sync(user):
	reminders = Reminder.objects.filter(user = user.id).order_by('-time')
	available_spots = user.maximum_reminders
	next_sync_time = watervibe_time.date_for_string(user.next_sync_time)
	for reminder in reminders:
		if watervibe_time.date_for_string(reminder.time) > next_sync_time:
			available_spots = available_spots - 1
		else:
			break

	return available_spots

def create_reminder(time, user):
	print "Adding reminder at " + watervibe_time.string_for_date(time)
	reminder = Reminder.objects.create(time= watervibe_time.string_for_date(time),
							user= user)
	reminder.save()


def last_reminder_for_user(user):
	return Reminder.objects.filter(user = user.id).last()

def time_between_reminders_for_user(user):
	return timedelta(hours= 1, minutes=30)

def reminder_count(user):
	return Reminder.objects.filter(user = user.id).count()

def create_reminders_for_user(user):
	print "Adding reminders..."
	available_reminders = reminders_available_at_next_sync(user)
	start_of_period, end_of_period = users.period_for_user(user)

	for x in range(0, available_reminders):
		last_reminder = last_reminder_for_user(user)
		
		if last_reminder is None:
			now = watervibe_time.now_in_user_timezone(user)
			next_reminder_time = start_of_period
			next_reminder_date = now
			
			next_reminder_date = next_reminder_date.replace(hour = next_reminder_time.hour, 
									   					  minute = next_reminder_time.minute)

			print "%s is the first alarm" % watervibe_time.string_for_date(next_reminder_date)
			while next_reminder_date < now:
				next_reminder_date = next_reminder_date + time_between_reminders_for_user(user)

				if next_reminder_date.hour > end_of_period.hour:
					next_reminder_date += timedelta(days = 1)
					next_reminder_date = next_reminder_date.replace(hour = start_of_period.hour,
											 minute  = start_of_period.minute)
		else:
			last_reminder_date = watervibe_time.date_for_string(last_reminder.time)
			next_reminder_date = last_reminder_date + time_between_reminders_for_user(user)

			if next_reminder_date.hour > end_of_period.hour:
				next_reminder_date = last_reminder_date + timedelta(days = 1)
				next_reminder_date = next_reminder_date.replace(hour = start_of_period.hour,
									    minute  = start_of_period.minute)


		create_reminder(next_reminder_date, user)