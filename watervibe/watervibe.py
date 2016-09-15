from .models import User
from tasks import setup

def register_fitbit_user(fitbit_user):
	 user = User.objects.create(app = 'fitbit',
							   app_id = fitbit_user.id
							  )
	 print "Created new user!"
	 user.save()
	 setup.delay(user)