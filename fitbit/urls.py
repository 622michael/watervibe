from django.conf.urls import url
from . import authorization

urlpatterns = [
	url(r'^authorize', authorization.authorize, name='authorize')
]