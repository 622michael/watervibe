from . import views
from .models import User
import json, requests

client_id = "227RR9"
access_token_request_url = "https://api.fitbit.com/oauth2/token"
base_64_clinet_id_secret_encode = "MjI3UlI5OjM1ZGE4N2RmYTViNTUwZWViZTYzY2NkZmEyOTlmZjY2"

def authorize (request):

	access_info, errors = request_access_info(request.GET['code'])
	if errors is not None:
		return views.authorization_failed(errors)

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

	return views.authorization_success()

def request_access_info (code, grant_type = "authorization_code"):
	parameters = {'code': code, 'grant_type': grant_type, 'client_id': client_id}
	headers = {"content-type":"application/x-www-form-urlencoded", "Authorization": "Basic " + base_64_clinet_id_secret_encode}
	response = requests.post(access_token_request_url, headers= headers, data= parameters)
	json_response = json.loads(response.content)
	if json_response.get('success', True) is False:
		return None, json_response['errors']

	return json_response, None