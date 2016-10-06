from .models import Device, User, Sleep
import alarms
import fitbit_time
import authorization


# This module is tasked with managing requests from
# Outside of the app. This includes converting watervibe
# Datatypes to one's readable by fitbit

## Outdated. Any app that access this information
## would have to have some knowledge of the Device
## model. Either it's usage should be done in the
## FitBit app itself or the task should not be done.

def devices_for_user(user):
	devices = Device.objects.filter(user=user.id)
	return devices

## Set Alarm
## --------------------------
## Takes a datetime object and 
## Calls the FitBit API to register
## on the alarm. Returns the alarm.id
## if it is successful. Returns None if
## unsuccessful.

def set_alarm (user_id, time):
	user = User.objects.get(id = user_id)

	day_int = time.isoweekday()
	day = fitbit_time.convert_isoweekday_to_string(day_int)

	for device in devices_for_user(user):
		alarm = alarms.set_alarm(user, device, time, day)

	if alarm is not None:
		return alarm.id
	else:
		return None

def max_reminders():
	return 8

##	Available Reminders For User
##  --------------------------
##	FitBit only lets os many alarms be set on the
##  device. This is how many are available to be
##  set.

def available_reminders_for_user(user_id):
	user = User.objects.get(id = user_id)

	return 8 - alarms.user_alarms_count(user)

## 	Weight For User
##  --------------------------
##  Gives the users weight in a float

def weight_for_user (user_id):
	user = User.objects.get(id = user_id)

	return user.weight

##	Sleep Times
##  --------------------------
##	Gives the times the user woke up	
## 	and the time that they went to bed. 
## 	Returns a list of list. The first is the sleep
## 	times the second is the times they woke up.

def sleep_times (user_id, day_of_the_week = None):
	try: 
		user = User.objects.get(id = user_id)
	except:
		return None, None

	start_times = []
	end_times = []

	for sleep in Sleep.objects.filter(user = user):
		if day_of_the_week is not None:
			if day_of_the_week is fitbit_time.date_for_string(sleep.start_time).isoweekday():
				start_times.append(sleep.start_time)
				end_times.append(sleep.end_time)
		else:
				start_times.append(sleep.start_time)
				end_times.append(sleep.end_time)

	return start_times, end_times

