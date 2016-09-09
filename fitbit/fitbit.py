import models
		
def devices_for_user(user):
	try:
		devices = Device.objects.get(user_id=user.id)
		return devices
	except:
		return None
