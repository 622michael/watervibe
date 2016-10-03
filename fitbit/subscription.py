from django.http import HttpResponse, HttpResponseRedirect

def sleep_notification (request):
	if not request.GET.get(verify, "") == "":
		if request.GET.get(verify, "") == "3007b326a29814af227edab671c5ae12315ef15f571d01485bccc33b3f9c8a23":
			return HttpResponse(status=204)
		else
			return HttpResponse(status=404)