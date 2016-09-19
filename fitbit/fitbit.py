from .models import Device, User
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

	device = devices_for_user(user).first()

	alarm = alarms.set_alarm(user, device, time, day)

	if alarm is not None:
		return alarm.id
	else:
		return None

def available_reminders_for_user(user_id):
	user = User.objects.get(id = user_id)

	return 2 - alarms.user_alarms_count(user)