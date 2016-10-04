from datetime import datetime, timedelta
from reminders import last_reminder_for_user
import dateutil
import users
import reminders

seconds_in_a_day = 86400.0

def string_for_day(day): 
	if day is 1:
		return "MONDAY"
	elif day is 2:
		return "TUESDAY"
	elif day is 3:
		return "WEDNESDAY"
	elif day is 4:
		return "THURSDAY"
	elif day is 5:
		return "FRIDAY"
	elif day is 6:
		return "SATURDAY"
	elif day is 7:
		return "SUNDAY"

def date_for_string(string):
	if len(string) > 11:
		date = datetime.strptime(remove_timezone_from_string(string), "%Y-%m-%d %H:%M")
	else:
		date = datetime.strptime(remove_timezone_from_string(string), "%H:%M")
	date = date.replace(tzinfo = dateutil.tz.tzoffset(None, hours_offset(string)*60*60))
	return date

def string_for_date(date):
	try:
		offset = date.utcoffset().total_seconds()/60/60
	except:
		offset = 0.0

	time = "%(hour)02d:%(minute)02d" % {'hour': date.hour, 'minute': date.minute}
	if offset < 0:
		utc_offset_string = "-%02d:00" % abs(offset)
	else:
		utc_offset_string = "+%02d:00" % abs(offset)

	time = time + utc_offset_string

	date = "%(year)02d-%(month)02d-%(day)02d " % {'year': date.year, 'month': date.month, 'day': date.day}

	return date + time

def remove_timezone_from_string(string):
	return string[:-6]

def time_zone_offset (string):
	return string[-6:]

def hours_offset (string):
	return int(time_zone_offset(string) [:3])

def time_till_sync(user):
	sync_datetime = date_for_string (user.next_sync_time)
	time_till_sync = sync_datetime - now_in_user_timezone(user)
	return time_till_sync

def seconds_till_sync(user):
	return time_till_sync(user).total_seconds()

def seconds_till_reminder(reminder):
	return (date_for_string(reminder.time) - now_in_user_timezone(reminder.user)).total_seconds()

def time_till_update(user):
	next_reminder = reminders.next_reminder_for(user)
	if next_reminder is None:
		return time_till_sync(user)

	next_reminder_time = date_for_string(next_reminder.time)
	time_till_update = next_reminder_time - now_in_user_timezone(user)
	return time_till_update


def seconds_till_update(user):
	return time_till_update(user).total_seconds()

def now_in_user_timezone(user):
	date = datetime.utcnow() + timedelta(hours=hours_offset(user.start_of_period))
	return date.replace(tzinfo = users.user_timezone(user))

# Supports Event times right now
def time_is_between_period (time, start_time, end_time):
	if start_time > end_time: ## Loops around the clock (ex. 8pm-3am)
		if time > start_time:
			return True
		else:
			adjusted_end_time = 24 + end_time 
			adjusted_time = 24 + time
			if adjusted_time < adjusted_end_time and adjusted_time > start_time:
				return True
	else:
		if time > start_time and time < end_time:
			return True

	return False

def event_time_from_date(date):
	hour = date.hour
	minute = float(date.minute)/60.0

	return hour + minute

