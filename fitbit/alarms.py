from .models import User, Device, Alarm
from device import first_device_for
import authorization
import json, requests
import fitbit
import fitbit_time
import datetime
from datetime import timedelta

add_alarm_url = "https://api.fitbit.com/1/user/-/devices/tracker/*/alarms.json"
delete_alarm_url = "https://api.fitbit.com/1/user/-/devices/tracker/*/alarms/$.json"

##	Set Alarm
##  --------------------------------------
##	Sets an alarm for the user on the given
##  date. FitBit sets alarms by day of the
##  week, so alarms should not be set a
##  week in advance.
def set_alarm (user, device, date, day):
	fitted_alarm_url = add_alarm_url.replace("-", user.fitbit_id).replace("*", device.fitbit_id)
	headers = authorization.api_request_header_for(user)
	fitbit_t = fitbit_time.time_from_date(date)
	print "Setting alarm for " + fitbit_t
	parameters = {'time': fitbit_t, 'enabled': "true", 'recurring': "false", 'weekDays': day}
	response = requests.post(fitted_alarm_url, headers= headers, data=parameters)

	json_response = json.loads(response.content)

	try:
		json_response = json_response["trackerAlarm"]
		alarm_id = json_response["alarmId"]
		alarm_time = fitbit_time.string_for_date(date)
		alarm = Alarm.objects.create(fitbit_id=alarm_id,
									 time= alarm_time,
									 user=user,
									 device=device)
		alarm.save()
	except:
		try:
			if json_response["errors"][0]["fieldName"] == 'deviceId':
				# Device probably doesn't support alarms
				device.delete()
				return None
			elif json_response["errors"][0]["message"] == "Cannot add more than 8 alarms to tracker.":
				alarms_cleared = clear_used_alarms_on_device(user, device)
				if alarms_cleared == True:
					return set_alarm(user, device, date, day)
				print "Failed to set alarm for %s. No spots." % fitbit_t
				return None
			else:
				print "Failed to set alarm for %s. %s" % (fitbit_t, json_response)
				return None
		except:
			# Often an authorization error
			print "Failed to set alarm for %s: %s" % (fitbit_t, json_response)
			return None

	print "Success."
	return alarm


##	User Alarms
##  --------------------------------------
##	Returns the number of alarms set on the user's
##	Device which were not set by the app
##
def user_alarms_count(user):
	device = first_device_for(user)
	fitted_alarm_url = add_alarm_url.replace("-", user.fitbit_id).replace("*", device.fitbit_id)
	headers = authorization.api_request_header_for(user)
	response = requests.get(fitted_alarm_url, headers= headers)
	json_response = json.loads(response.content)

	try:
		alarms = json_response["trackerAlarms"]
		count = 0

		for alarm in alarms:
			try:
				Alarm.objects.get(fitbit_id = alarm["alarmId"])
			except:
				count += 1
		
		return count

	except:
		return json_response["errors"]

##	Delete Alarm
##  --------------------------------------
##  Deletes alarm from FitBit
def delete_alarm(user, device, alarm):
	print "Deleting: " + alarm.time
	fitted_alarm_url = delete_alarm_url.replace("-", user.fitbit_id).replace("*", device.fitbit_id).replace('$', alarm.fitbit_id)
	headers = authorization.api_request_header_for(user)
	
	requests.delete(fitted_alarm_url, headers=headers)
	alarm.delete()

##	Clear Used Alarms on Device
##  --------------------------------------
##  Deletes every alarm from the device
##  that has already passed.
def clear_used_alarms_on_device (user, device):
	result = False
	try:
		alarms = Alarm.objects.filter(user=user.id, device=device.id)
		for alarm in alarms:
			now_in_user_time = datetime.datetime.now() + timedelta(hours = fitbit_time.timezone_offset(alarm.time))
			if fitbit_time.date_for_string(alarm.time) < now_in_user_time:
				delete_alarm(user, device, alarm)
				result = True
		return result
	except:
		return result

