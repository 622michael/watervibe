from models import Reminder, User
from datetime import datetime, date, timedelta
from watervibe_time import time_zone_offset, date_for_string, hours_offset, string_for_date, now_in_user_timezone
import dateutil.parser
import importlib


def calculate_stats(user): 
	user.start_of_period = calculate_start_period(user)
	user.end_of_period = calculate_end_period(user)
	user.ounces_in_a_day = calculate_ounces_in_a_day(user)
	user.drink_size = calculate_drink_size(user)
	user.next_sync_time = calculate_sync_time(user)
	user.maximum_reminders = calculate_maximum_reminders(user)
	user.save()

def calculate_start_period(user):
	default_start_value = '08:30-04:00'
	return default_start_value

def calculate_end_period(user):
	default_end_value = '20:30-04:00'
	return default_end_value

def calculate_ounces_in_a_day(user):
	default_ounces_in_a_day = 64.0
	return default_ounces_in_a_day

def calculate_drink_size(user):
	default_drink_size = 8.0
	return default_drink_size

def calculate_sync_time(user):
	tomorrow = date.today() + timedelta(days=1)
	default_sync_time = "%(year)02d-%(month)02d-%(day)02d 00:00-04:00" % {'year': tomorrow.year, 'month': tomorrow.month, 'day': tomorrow.day}
	return default_sync_time

def calculate_maximum_reminders(user):
	app = importlib.import_module(user.app + "." + user.app)
	return app.available_reminders_for_user(user.app_id)

def start_of_period (user):
	return date_for_string(user.start_of_period)

def end_of_period (user): 
	return date_for_string(user.end_of_period)

def period_for_user (user):
	start_time =  start_of_period(user)
	end_time = end_of_period(user)
	return start_time, end_time

def maximum_reminders(user):
	user_app = importlib.import_module(user.app + "." + user.app)
	return user_app.max_reminders()

def user_timezone(user): 
	return dateutil.tz.tzoffset(None, hours_offset(user.start_of_period)*60*60)

##	Maximum Time Between Reminders
##  --------------------------------------
##	Calculates how much time must be
##  Between reminders in order for the
##  Base amount of ounces is met.
def maximum_time_between_reminders(user):
	return timedelta(hours = 1, minutes = 30)

##	Reminders at next sync
##  --------------------------------------
##	A list of reminders that will not have
##  Fired at the next sync time.
## 
def reminders_at_next_sync(user):
	all_reminders = user_reminders(user).order_by("-time")
	reminders = []
	next_sync_time = date_for_string(user.next_sync_time)

	for reminder in all_reminders:
		time = date_for_string(reminder.time)
		if time > next_sync_time:
			print "%s is after %s" % (time, next_sync_time) 
			reminders.append(reminder)
		else:
			print "%s is before %s" % (time, next_sync_time)
			break

	return reminders

def reminders_availabe_at_next_sync(user):
	available_spots = maximum_reminders(user)
	return available_spots - reminders_at_next_sync(user).count()

def user_reminders(user):
	return Reminder.objects.filter(user_id = user.id)

