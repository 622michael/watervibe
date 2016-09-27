from .models import User
import authorization
import json, requests

profile_url = "https://api.fitbit.com/1/user/-/profile.json"
##	Profile
##  --------------------------------------
##	Returns the json response from the 
## 	FitBit API profile call.
##
def profile(user):
	fitted_profile_url = "https://api.fitbit.com/1/user/-/profile.json".replace("-", user.fitbit_id)
	headers = authorization.api_request_header_for(user)
	response = requests.post(fitted_profile_url, headers= headers)
	json_response = json.loads(response.content)

	return json_response["user"]

##	Update Profile
##  --------------------------------------
##	Stores all relavent information from
##	FitBit API profile call and stores it
##	In the relavent user fields.
def update_profile(user):
	user_profile = profile(user)
	update_weight(user, user_profile)
	user.save()

##	Update Weight
##  --------------------------------------
##	Loads a new weight into user.weight
## 	From the FitBit API profile call.
##
def update_weight (user, user_profile):
	weight = float(user_profile["weight"])

	if user_profile["weightUnit"] == "METRIC":
		weight = weight * 2.2046226218
		
	user.weight = weight
	user.save()