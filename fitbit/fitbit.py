from .models import Device
from . import alarms
		
def devices_for_user(user):
	devices = Device.objects.filter(user=user.id)
	return devices

def set_alarm_for_user_device_time(user, device, time):
	alarms.set_alarm_for(user, device, time)