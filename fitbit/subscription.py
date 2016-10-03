from django.http import HttpResponse, HttpResponseRedirect
import authorization
import json, requests

subscribe_url = "https://api.fitbit.com/1/user/-/*/apiSubscriptions/!.json"

## A dictionary of all the notification types
## The key is the name of the notification type
## The value is the fitbit id that links the subscribtion
## to the proper server url.
notification_types = {"sleep": 1}

## Contacts FitBit API and subscribes
## the server to recieve updates on a
## certain piece of health information
## notification_type must be "sleep" for now
def subscribe(user, notification_type):
	fitbit_subscription_id = "%d" % notification_types[notification_type]
	fitted_subscribe_url = subscribe_url.replace('-', user.fitbit_id).replace('*', notification_type).replace('!', fitbit_subscription_id)
	headers = authorization.api_request_header_for(user)
	headers["X-Fitbit-Subscriber-Id"] = fitbit_subscription_id
	response = requests.post(fitted_subscribe_url, headers= headers)


## Called by the FitBit API notifying
## the server with new sleep information
##

def sleep_notification (request):
	if not request.GET.get("verify", "") == "":
		if request.GET.get("verify", "") == "3007b326a29814af227edab671c5ae12315ef15f571d01485bccc33b3f9c8a23":
			return HttpResponse(status=204)
		else:
			return HttpResponse(status=404)

	print "Request of new notfication:"
	print request
	return HttpResponse(status = 204)
