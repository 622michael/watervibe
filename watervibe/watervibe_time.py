from datetime import datetime, timedelta

def date_for_string(string):
	return datetime.strptime(remove_timezone_from_string(string), "%Y-%m-%d %H:%M")

def string_for_date(date, offset=0):
	time = "%02d:%02d"
	if utc_offset < 0:
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
	sync_datetime = date_for_string (user.next_sync_time) + timedelta(hours=hours_offset(user.next_sync_time))
	time_till_sync = sync_datetime - datetime.now()
	return time_till_sync

def seconds_till_sync(user):
	return time_till_sync(user).total_seconds()