from .models import Device
import alarms
import fitbit_time


# This module is tasked with managing requests from
# Outside of the app. This includes converting python
# Datatypes to one's readable by fitbit


def devices_for_user(user):
	devices = Device.objects.filter(user=user.id)
	return devices

def set_alarm_for_user_device_time(user, device, time):
	day_int = time.isoweekday()
	day = fitbit_time.convert_isoweekday_to_string(day_int)

	alarms.set_alarm(user, device, time, day)
