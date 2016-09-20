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

def period_for_user (user):
	start_time =  date_for_string(user.start_of_period)
	end_time = date_for_string(user.end_of_period)
	return start_time, end_time

def user_timezone(user): 
	return dateutil.tz.tzoffset(None, hours_offset(user.start_of_period)*60*60)

def reminders_availabe_at_next_sync(user):
	reminders = reminders(user).order_by('-time')
	available_spots = user.maximum_reminders
	next_sync_time = date_for_string(user.next_sync_time)
	for reminder in reminders:
		if reminder.time > next_sync_time:
			available_spots = available_spots - 1
		else:
			break

	return available_spots

def reminders(user):
	return Reminder.objects.filter(user = user.id)

