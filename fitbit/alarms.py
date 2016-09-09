from .models import User, Device, Alarm
import authorization
import json, requests

add_alarm_url = "https://api.fitbit.com/1/user/-/devices/tracker/*/alarms.json"

def set_alarm_for (user, device, time):
	fitted_alarm_url = add_alarm_url.replace("-", user.fitbit_id).replace("*", device.fitbit_id)
	headers = authorization.api_request_header_for(user)
	parameters = {'time': time, 'enabled': "true", 'recurring': "false", 'weekDays': 'WEDNESDAY'}
	response = requests.post(fitted_alarm_url, headers= headers, data=parameters)
	json_response = json.loads(response.content)
	print json_response
	if json_response.get('success', True) is False:
		print "Failure"
		return None

	print "Success!"
	json_response = json_response["trackerAlarm"]
	alarm_id = json_response["alarmId"]
	alarm_time = json_response["time"]
	alarm = Alarm.objects.create(fitbit_id=alarm_id,
								 time= alarm_time,
								 user=user,
								 device=device)

	alarm.save()

	return alarm