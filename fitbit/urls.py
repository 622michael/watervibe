from django.conf.urls import url
from . import authorization, views

urlpatterns = [
	url(r'^authorize', authorization.authorize, name='authorize'),
	url(r'^button', views.permission_button, name='button'),
	url(r'^subscribe', authorization.permissions_request, name='permissions'),
]