from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
# from . import authorization
import authorization

# Create your views here.

def authorization_success(scope, request):
	return render(request, 'fitbit/success.html', {})

def authorization_failed(errors, request):
	return render(request, 'fitbit/failed.html', {})


def permission_button(request):
	return render(request,'fitbit/button.html', {})


def request_permissions(request): 
	redirect_reponse = authorization.permissions_request()
	return redirect_reponse
