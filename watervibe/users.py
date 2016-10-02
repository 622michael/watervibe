from models import Reminder, User, Time
from datetime import datetime, date, timedelta
from watervibe_time import time_zone_offset, date_for_string, hours_offset, string_for_date, now_in_user_timezone
import dateutil.parser
import importlib
import math
import stats

def users():
	return User.objects.all()

def calculate_stats(user): 
	user.start_of_period = calculate_start_period(user)
	user.end_of_period = calculate_end_period(user)
	user.ounces_in_a_day = calculate_ounces_in_a_day(user)
	user.drink_size = calculate_drink_size(user)
	user.next_sync_time = sync_time(user)
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

def sync_time(user):
	an_hour_from_now = now_in_user_timezone(user) + timedelta(hours = 1)
	beginning_of_hour = an_hour_from_now.replace(minute = 0) # Sets to beginning of hour
	return string_for_date(beginning_of_hour)

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

def period_for_date (user, date):
	start_time, end_time = period_for_user(user)
	start_date = start_time.replace(day = date.day, 
									month = date.month, 
									year = date.year)
	end_date = end_time.replace(day = date.day,
								month = date.month,
								year = date.year)

	return start_date, end_date

def ounces_in_period (user, start_date, end_date):
	app = importlib.import_module(user.app + "." + user.app)
	weight = app.weight_for_user(user.app_id)

	base_ounces = (2.0/3.0) * weight

	return base_ounces


def maximum_reminders(user):
	user_app = importlib.import_module(user.app + "." + user.app)
	return user_app.max_reminders()

def user_timezone(user): 
	return dateutil.tz.tzoffset(None, hours_offset(user.start_of_period)*60*60)

def ounces_to_drink_in_period(user, start_date, end_date):
	reminders = user_reminders(user).order_by("-time")
	count = 0
	for reminder in reminders:
		reminder_date = date_for_string(reminder.time)
		if reminder_date > start_date and reminder_date < end_date:
			count += 1

	return count * user.drink_size


##	Weighted Average Wake Time
##  --------------------------------------
##	The average time that the user wakes up
##	with an unset weight attached to the data
##	that should decrease as the data gets further away (TODO)
def weighted_average_wake_time(user, day_of_the_week):
	app = importlib.import_module(user.app + "." + user.app)
	wake_times = app.wake_times(user.app_id)
	parsed_times = []
	for wake_time in wake_times:
		date = date_for_string(wake_time)
		if date.isoweekday() == day_of_the_week:
			time = float(date.hour) + float(date.minute)/60.0
			parsed_times.append(time)

	return stats.weighted_average(parsed_times, lambda x: 1)


##	Weighted Average Sleep Time
##  --------------------------------------
##	The average time that the user wakes up
##	with an unset weight attached to the data
##	that should decrease as the data gets further away (TODO)
def weighted_average_sleep_time(user, day_of_the_week):
	app = importlib.import_module(user.app + "." + user.app)
	sleep_times, wake_times = app.sleep_times(user.app_id)
	parsed_times = []
	for sleep_time in sleep_times:
		date = date_for_string(sleep_time)
		if date.isoweekday() == day_of_the_week:
			time = float(date.hour) + float(date.minute)/60.0
			parsed_times.append(time)

	return stats.weighted_average(parsed_times, lambda x: 1)


##	Maximum Time Between Reminders
##  --------------------------------------
##	Calculates how much time must be
##  Between reminders in order for the
##  Base amount of ounces is met.
##  Input: user -> watervibe_user, date -> datetime
def maximum_time_between_reminders(user, date):
	minutes_in_a_day = 60*24
	minutes_asleep_in_day = 0
	for time in Time.objects.all():
		probability_of_sleeping = stats.probability("sleep", 
													time, 
													user = user, 
													day_of_week = date.isoweekday())

		if probability_of_sleeping > 0.25: 
			minutes_asleep_in_day += 1

	minutes_for_reminders = minutes_in_a_day - minutes_asleep_in_day
	seconds_for_reminders = minutes_for_reminders * 60

	start_of_period = date.replace( hour = 0, minute = 0, second = 0)
	end_of_period = start_of_period + timedelta(days = 1)

	ounces = ounces_in_period (user, start_of_period, end_of_period)
	
	drink_size = user.drink_size

	length_of_period = minutes_for_reminders
	num_reminders = ounces/drink_size

	time_between_reminders = length_of_period/num_reminders
	return timedelta(seconds = length_of_period/num_reminders)

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
			reminders.append(reminder)
		else:
			break

	return reminders

##	Reminders available at next sync
##  --------------------------------------
##	An integer for the amount of available
##	spots when the next sync occurs.
## 
def reminders_availabe_at_next_sync(user):
	available_spots = maximum_reminders(user)
	return available_spots - reminders_at_next_sync(user).count()

def user_reminders(user):
	return Reminder.objects.filter(user_id = user.id)

