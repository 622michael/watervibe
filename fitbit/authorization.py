from . import device, alarms
import views
from .models import User 
import json, requests
import urllib
from django.http import HttpResponse, HttpResponseRedirect
import datetime
import webbrowser
from watervibe import vibes_setter

client_id = "227RR9"
scope_request_url = "https://www.fitbit.com/oauth2/authorize?"
access_token_request_url = "https://api.fitbit.com/oauth2/token"
base_64_clinet_id_secret_encode = "MjI3UlI5OmMxYmI3YWNmNTI5YjJkZTA2ODk1YWU1YzM4N2RmYzAx"
api_scope = ["activity", "heartrate", "location", "profile", "settings", "sleep", "weight"]



def authorize (request):

	access_info, errors = request_access_info(request.GET['code'])
	if errors is not None:
		return views.authorization_failed(errors, request)

	user_id = access_info["user_id"]
	access_token = access_info["access_token"]
	scope = access_info["scope"]
	refresh_token = access_info["refresh_token"]

	print scope

	try:
		user = User.objects.get(fitbit_id=user_id)
		user.access_token = access_token
		user.scope = scope
		user.refresh_token = refresh_token
		user.save()
	except:
		user = User.objects.create( fitbit_id=user_id, 
								access_token=access_token, 
								scope=scope, 
								refresh_token=refresh_token)
		user.save()

	
	device.get_devices_for(user)
	vibes_setter.add_vibes_for_next_period_for_user(user)

	return views.authorization_success(scope, request)

def permissions_request(request):
	base_url = scope_request_url
	scope = ""
	for data_point in api_scope: 
		scope += data_point + " "

	parameters = {"client_id": client_id, "scope": scope, "response_type": "code"}

	url = base_url + urllib.urlencode(parameters)

	redirect_reponse = HttpResponse("", status=302)
	redirect_reponse["location"] = url 
	return redirect_reponse


def request_access_info (code, grant_type = "authorization_code"):
	parameters = {'code': code, 'grant_type': grant_type, 'client_id': client_id}
	headers = {"content-type":"application/x-www-form-urlencoded", "Authorization": "Basic " + base_64_clinet_id_secret_encode}
	response = requests.post(access_token_request_url, headers= headers, data= parameters)
	json_response = json.loads(response.content)
	if json_response.get('success', True) is False:
		print json_response
		return None, json_response['errors']

	return json_response, None

def api_request_header_for(user):
	headers = {'Authorization': 'Bearer ' + user.access_token}
	return headers