from .models import Device, User, Sleep
import alarms
import fitbit_time
import authorization


# This module is tasked with managing requests from
# Outside of the app. This includes converting python
# Datatypes to one's readable by fitbit


def devices_for_user(user):
	devices = Device.objects.filter(user=user.id)
	return devices

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

def available_reminders_for_user(user_id):
	user = User.objects.get(id = user_id)

	return 8 - alarms.user_alarms_count(user)

def weight_for_user (user_id):
	user = User.objects.get(id = user_id)

	return user.weight

def wake_times (user_id):
	times = []
	for sleep in Sleep.objects.filter(user_id = user_id):
		if sleep.is_main_sleep:
			times.append(sleep.end_time)

	return times
