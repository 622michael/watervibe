from .models import User, Sleep
import authorization
import json, requests
from fitbit_time import string_for_date, now, log_date_for_string
from datetime import timedelta

profile_url = "https://api.fitbit.com/1/user/-/profile.json"
sleep_log_url = "https://api.fitbit.com/1/user/-/sleep/date/*.json"

##	Profile
##  --------------------------------------
##	Returns the json response from the 
## 	FitBit API profile call.
##
def profile(user):
	fitted_profile_url = "https://api.fitbit.com/1/user/-/profile.json".replace("-", user.fitbit_id)
	headers = authorization.api_request_header_for (user)
	response = requests.post (fitted_profile_url, headers= headers)
	json_response = json.loads (response.content)

	return json_response["user"]

##	Update Profile
##  --------------------------------------
##	Stores all relavent information from
##	FitBit API profile call and stores it
##	in the relavent user fields.
def update_profile(user):
	user_profile = profile(user)
	update_weight(user, user_profile)
	user.save()

##	Update Weight
##  --------------------------------------
##	Loads a new weight into user.weight
## 	from the FitBit API profile call.
##

def update_weight (user, user_profile):
	weight = float(user_profile["weight"])

	if user_profile["weightUnit"] == "METRIC":
		weight = weight * 2.2046226218
		
	user.weight = weight
	user.save()

##	Update Sleep Log
##  --------------------------------------
##	Loads and stores all sleep logs since
##	the last time they were loaded. Loads
##	into fitbit.sleep.

def sync_sleep_logs (user): 
	last_sleep_sync = user.last_sleep_sync

	if last_sleep_sync is None:
		last_sleep_sync = now() - timedelta(days = 30)

	days_since_last_sleep_sync = (now() - last_sleep_sync).days

	for x in range(1, days_since_last_sleep_sync):
		date = last_sleep_sync + timedelta(days = x)
		new_sleep_log = sleep_log(user, date)
		for sleep in new_sleep_log:
			log_id = sleep["logId"]
			try:
				sleep = Sleep.get(fitbit_id = log_id)
			except:
				main_sleep = sleep["isMainSleep"]
				start_time = log_date_for_string(sleep["startTime"])
				duration   = int(sleep["duration"])
				end_time   = start_time + timedelta(seconds = duration)

				s = Sleep.objects.create (is_main_sleep = main_sleep,
							  fitbit_id  = log_id,
							  start_time = string_for_date(start_time),
							  duration 	 = duration,
							  end_time	 = string_for_date(end_time),
							  user       = user)
				s.save()

	user.last_sleep_sync = string_for_date(now())
	user.save()


##	Sleep Log
##  --------------------------------------
##	Returns the sleep log for the given
## 	date from the FitBit API sleep log
##  call.

def sleep_log (user, date):
	date_string = string_for_date (date, time = False)
	fitted_sleep_url = sleep_log_url.replace ("-", user.fitbit_id).replace("*", date_string)
	headers = authorization.api_request_header_for (user)
	response = requests.get (fitted_sleep_url, headers = headers)
	json_response = json.loads(response.content)

	print json_response
	return json_response["sleep"]

##	Sleep Logs
##  --------------------------------------
##	Returns all sleep logs for the given
##	User. 
##

def sleep_logs(user):
	return Sleep.objects.filter(user = user.id)