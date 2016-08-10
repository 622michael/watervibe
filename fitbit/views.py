from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def authorization_success():
	redirect_reponse = HttpResponse("", status=302)
	redirect_reponse["location"] = "watervibe://fitbit/success"
	return redirect_reponse

def authorization_failed(errors):
	redirect_reponse = HttpResponse("", status=302)
	redirect_reponse["location"] = "watervibe://fitbit/failed"
	return redirect_reponse
