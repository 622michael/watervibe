from .models import Device
import alarms
import pytz

# This module is tasked with managing requests from
# Outside of the app. This includes converting python
# Datatypes to one's readable by fitbit

def convert_isoweekday_to_string(isoweekday):
	if isoweekday is 1:
		return "MONDAY"
	elif isoweekday is 2:
		return "TUESDAY"
	elif isoweekday is 3:
		return "WEDNESDAY"
	elif isoweekday is 4:
		return "THURSDAY"
	elif isoweekday is 5:
		return "FRIDAY"
	elif isoweekday is 6:
		return "SATURDAY"
	elif isoweekday is 7:
		return "SUNDAY"

		
def devices_for_user(user):
	devices = Device.objects.filter(user=user.id)
	return devices

def set_alarm_for_user_device_time(user, device, time):
	utc_offset = int(time.utcoffset().total_seconds()/3600)
	utc_offset_string = ""
	if utc_offset < 0:
		utc_offset_string = "-%02d:00" % abs(utc_offset)
	else:
		utc_offset_string = "+%02d:00" % abs(utc_offset)

	fitbit_time = "%02d:%02d"%(time.hour, time.minute) + utc_offset_string
	print fitbit_time

	day_int = time.isoweekday()
	day = convert_isoweekday_to_string(day_int)

	alarms.set_alarm_for(user, device, fitbit_time, day)