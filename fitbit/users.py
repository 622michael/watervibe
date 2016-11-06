from .models import User, Sleep
import authorization
import json, requests
from fitbit_time import string_for_date, now, log_date_for_string, date_for_string
from datetime import timedelta
from pytz import timezone
import dateutil
from watervibe import watervibe

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
	print json_response

	return json_response["user"]

##	Update Profile
##  --------------------------------------
##	Stores all relavent information from
##	FitBit API profile call and stores it
##	in the relavent user fields.

def update_profile(user):
	try:
		user_profile = profile(user)
		update_weight(user, user_profile)
		update_timezone(user, user_profile)
		update_name(user, user_profile)
		user.save()
	except:
		pass

##  Update Timezone
## --------------------------------------
##	Loads new timezone infomration into
##	user.timezone. Sets as a UTC offset

def update_timezone(user, user_profile):
	user.timezone = user_profile["timezone"]

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

##	Update Name
##  --------------------------------------
##	Seperates the name from the FitBit API
##  by space. The first is the first name;
##	the rest is the last name.

def update_name(user, user_profile):
	words = user_profile["fullName"].split()
	first_name = words[0]
	words.remove(first_name)
	last_name =  " ".join(words)

	user.first_name = first_name
	user.last_name = last_name

##	Update Weight
##  --------------------------------------
##	Loads a new city,state into user.city
## 	and user.state from the FitBit API 
##	profile call.

def update_location(user, user_profile):
	user.city = user_profile["city"]
	user.state = user_profile["state"]



##  Sync Logs Of Type
##  --------------------------------------
##  Loads and stores all logs of a certain
##  the last time they were loaded. Loads
##  into fitbit_{type}.

def sync_logs_of_type(user, type):
	try:
		last_sync = date_for_string(getattr(user, "last_%s_sync" % type)).replace(tzinfo = dateutil.tz.tzoffset(None, 0))
	except:
		last_sync = now() - timedelta(days = 30)

	days_since_last_sync = (now() - last_sync).days

	for x in range(1, days_since_last_sync):
		date = last_sync + timedelta(days = x)
		new_log = globals()[type + "_log"](user, date)
		for log in new_log:
			log_id = log["logId"]
			globals()["create_%s_from_log" % type](user, log)
				

	user.last_sleep_sync = string_for_date(now())
	user.save()


##	Sync Sleep Logs
##  --------------------------------------
##	Loads and stores all sleep logs since
##	the last time they were loaded. Loads
##	into fitbit_sleep.

def sync_sleep_logs (user): 
	sync_logs_of_type(user, "sleep")


## 	Create Sleep From Log
## 	--------------------------------------
## 	Takes a json log from the the FitBit API
## 	for input. Creates a Sleep model if the
##	the log as not already been stored. Returns
##	True if the Sleep object is created or if
##	False if it already exists.

def create_sleep_from_log(user, sleep):
	log_id = sleep["logId"]

	try:
		sleep = Sleep.get(fitbit_id = log_id)
		return False
	except:
		main_sleep = sleep["isMainSleep"]
		start_time = log_date_for_string(user, sleep["startTime"])
		duration   = int(sleep["duration"])
		end_time   = start_time + timedelta(milliseconds = duration)

		s = Sleep.objects.create (is_main_sleep = main_sleep,
					  fitbit_id  = log_id,
					  start_time = string_for_date(start_time),
					  duration 	 = duration,
					  end_time	 = string_for_date(end_time),
					  user       = user)
		watervibe.register_sample ("fitbit", user.id, "sleep", day_of_the_week = start_time.isoweekday())

		s.save()
		return True



##	Sleep Log
##  --------------------------------------
##	Returns the sleep log for the given
## 	date from the FitBit API sleep log
##  call.

def sleep_log (user, date):
	date_string = string_for_date (date, time = False)
	fitted_sleep_url = sleep_log_url.replace("-", user.fitbit_id).replace("*", date_string)
	headers = authorization.api_request_header_for(user)
	response = requests.get(fitted_sleep_url, headers = headers)
	json_response = json.loads(response.content)

	try:
		return json_response["sleep"]
	except:
		return []

##	Sleep Logs
##  --------------------------------------
##	Returns all sleep logs for the given
##	User. 
##

def sleep_logs(user):
	return Sleep.objects.filter(user = user.id)



