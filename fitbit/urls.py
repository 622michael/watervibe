from django.conf.urls import url
from . import authorization, views, subscription

urlpatterns = [
	url(r'^authorize', authorization.authorize, name='authorize'),
	url(r'^button', views.permission_button, name='button'),
	url(r'^subscribe', authorization.permissions_request, name='permissions'),
	url(r'^notification/sleep', subscription.sleep_notification, name = 'sleep notification')
]
