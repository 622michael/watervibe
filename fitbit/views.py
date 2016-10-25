from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
# from . import authorization
import authorization

# Create your views here.

def authorization_success(request, alarms, sleep):
	return render(request, 'dashboard.html', {"alarms" : alarms, "sleep": sleep})

def authorization_failed(errors, request):
	return render(request, 'failed.html', {})


def permission_button(request):
	return render(request,'button.html', {})


def request_permissions(request): 
	redirect_reponse = authorization.permissions_request()
	return redirect_reponse

def alarms_full(request): 
	return error(request, "You have too many alarms on your FitBit (max is 8). Please remove at least one and register again.")

def error(request, message):
	return render(request, 'error.html', {'message' : message})


def handler500(request):
	return error(request, "An unknown error has occured. Please let watervibe.co@gmail.com know you have recieved this message. Thank you!")