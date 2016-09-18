import authorization
import json, requests
from .models import Device, User

devices_url = "https://api.fitbit.com/1/user/-/devices.json"

def get_devices_for(user):
	headers = authorization.api_request_header_for(user)
	response = requests.get(devices_url, headers = headers)
	json_response = json.loads(response.content)

	try:
		if json_response.get('success', True) is False:
			print 'Failed to get devices: ' + json_response['errors']
			return None
	except: 
		if json_response == []:
			print 'No devices'
			return None

	devices = []
	for device_directory in json_response:
		device_fitbit_id = device_directory["id"]
		device_version = device_directory["deviceVersion"]
		device_type = device_directory["type"]
		print device_fitbit_id
		try:
			device = Device.objects.get(fitbit_id = device_fitbit_id)
		except:
			device = Device.objects.create(fitbit_id = device_fitbit_id,
										version = device_version,
										device_type = device_type,
										user = user)
			devices.append(device)

	return devices

def first_device_for(user):
	return Device.objects.get(user=user.id)

