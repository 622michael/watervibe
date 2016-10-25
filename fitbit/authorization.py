import alarms
import device
import views
from .models import User 
import json, requests
import urllib
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, timedelta
import webbrowser
import watervibe.watervibe
import fitbit_time
import users
import subscription 
from django.conf import settings

client_id = "227RR9"
scope_request_url = "https://www.fitbit.com/oauth2/authorize?"
access_token_request_url = "https://api.fitbit.com/oauth2/token"
base_64_clinet_id_secret_encode = "MjI3UlI5OmMxYmI3YWNmNTI5YjJkZTA2ODk1YWU1YzM4N2RmYzAx"
api_scope = ["activity", "heartrate", "location", "profile", "settings", "sleep", "weight"]

##	Permissions Request
##  --------------------------------------
##	Loads the redirect to begin oauth process 
##
##

def permissions_request(request):
	base_url = scope_requesttests_url
	scope = ""
	for data_point in api_scope: 
		scope += data_point + " "

	parameters = {"client_id": client_id, "scope": scope, "response_type": "code"}
	url = base_url + urllib.urlencode(parameters)

	redirect_reponse = HttpResponse("", status=302)
	redirect_reponse["location"] = url 
	return redirect_reponse

##	Authorize
##  --------------------------------------
##	handles the request from the fitbit server	
##  after a new user authorizes the app
##
def authorize (request):

	access_info, errors = request_access_info(code = request.GET['code'])
	if errors is not None:
		return views.error(request, "Something went wrong authenticating with FitBit. Please try again.")

	user_id = access_info["user_id"]
	access_token = access_info["access_token"]
	scope = access_info["scope"]
	refresh_token = access_info["refresh_token"]
	expiration_date = fitbit_time.now() + timedelta(seconds = access_info["expires_in"])
	expiration_date = fitbit_time.string_for_date(expiration_date)

	try:
		user = User.objects.get(fitbit_id = user_id)
		user.access_token = access_token
		user.scope = scope
		user.refresh_token = refresh_token
		user.access_token_expiration = expiration_date
		user.save()

		alarm_times = watervibe.watervibe.fitbit_dashboard_alarms(user.id)
		sleep = watervibe.watervibe.fitbit_dashboard_sleep_times(user.id)

		return views.authorization_success(request, alarms_times, sleep)  
	except:
		user = User.objects.create( fitbit_id = user_id, 
								access_token = access_token, 
								scope = scope, 
								refresh_token = refresh_token)
		user.save()

	users.update_profile(user)
	devices = device.get_devices_for(user)

	if devices is None:
		return views.error(request, "No device on your FitBit account supports silent alarms. Please try again after adding a device to your FitBit account.")

	if "sleep" in user.scope:
		subscription.subscribe(user, "sleep")

	if(alarms.user_alarms_count(user) == 8): 
		print "User account is full"
		return views.alarms_full(request)

	watervibe.watervibe.register_fitbit_user(user)

	alarms = watervibe.watervibe.fitbit_dashboard_alarms(user.id)

	return views.authorization_success(request, alarms)

##	Refresh Access
##  --------------------------------------
##	uses the refresh token to refresh the access token	
##
##
def refresh_access_for_user(user):
	access_info, errors = request_access_info(refresh_token = user.refresh_token, grant_type = "refresh_token")
	if errors is not None:
		return None


	expiration_date = fitbit_time.now() + timedelta(seconds = access_info["expires_in"])
	
	user.access_token = access_info["access_token"]
	user.refresh_token = access_info["refresh_token"]
	user.access_token_expiration = fitbit_time.string_for_date(expiration_date)
	user.save()


##	Request Access Info
##  --------------------------------------
##	used get the user's authorization code 
##	param code is the code from fitbit server
##	returns access token, scope, refresh token	

def request_access_info (code = "", refresh_token = "", grant_type = "authorization_code"):
	parameters = {'code': code, 'grant_type': grant_type, 'client_id': client_id, 'refresh_token': refresh_token}
	headers = {"content-type":"application/x-www-form-urlencoded", "Authorization": "Basic " + base_64_clinet_id_secret_encode}
	response = requests.post(access_token_request_url, headers= headers, data= parameters)
	json_response = json.loads(response.content)
	if json_response.get('success', True) is False:
		return None, json_response['errors']

	return json_response, None

##	Request Header
##  --------------------------------------
##	returns the header necessary to make
## 	an api calls. It also refreshes the
##	access token if it is out of date

def api_request_header_for(user):
	expiration_date = fitbit_time.date_for_string(user.access_token_expiration)

	if expiration_date < datetime.now() and not settings.TESTING:
		refresh_access_for_user(user)

	headers = {'Authorization': 'Bearer ' + user.access_token}
	return headers
