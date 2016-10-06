from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from models import User
import authorization
import json, requests
import users

subscribe_url = "https://api.fitbit.com/1/user/-/*/apiSubscriptions/!.json"
subscriptions_url = "https://api.fitbit.com/1/user/-/sleep/apiSubscriptions.json"

## Notifications Types
## --------------------------------------
## A dictionary of all the notification types
## The key is the name of the notification type
## The value is the fitbit id that links the subscribtion
## to the proper server url.

notification_types = {"sleep": 1}

##  Subscribe To All Subscriptions 
##  --------------------------------------
##  Subscribes the user to all notifications
##  in the notifications types

def subscribe_to_all_subscriptions(user): 
	for service in notification_types.keys():
		subscribe(user, service)

##  Subscribe
##  --------------------------------------
## Contacts FitBit API and subscribes
## the server to recieve updates on a
## certain piece of health information
## notification_type must be "sleep" for now

def subscribe(user, notification_type):
	fitbit_subscription_id = "%d" % notification_types[notification_type]
	fitted_subscribe_url = subscribe_url.replace('*', notification_type).replace('!', fitbit_subscription_id)
	headers = authorization.api_request_header_for(user)
	headers["X-Fitbit-Subscriber-Id"] = fitbit_subscription_id
	response = requests.post(fitted_subscribe_url, headers= headers)

##	Sleep Notification
##  --------------------------------------
## Called by the FitBit API notifying
## the server with new sleep information
## Syncs all the lastest sleep logs for each
## User in the cal.

@csrf_exempt
def sleep_notification (request):
	if not request.GET.get("verify", "") == "":
		if request.GET.get("verify", "") == "3007b326a29814af227edab671c5ae12315ef15f571d01485bccc33b3f9c8a23":
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	updated_ids = []
	for update in request.body:
		fitbit_id = update["ownerId"]
		if fitbit_id in updated_ids:
			next
		try:
			user = Users.object.get(fitbit_id = fitbit_id)
		except:
			next

		users.sync_sleep_logs(user)
		updated_ids.append(user)

	return HttpResponse(status = 204)
