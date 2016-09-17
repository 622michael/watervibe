from .models import User
from tasks import setup

def register_fitbit_user(fitbit_user):
	try:
		user = User.objects.get(app_id = user_id)
		print "Already registered"
	except:
		user = User.objects.create(app = 'fitbit',
							   app_id = fitbit_user.id
							  )
	 	user.save()
	 	setup.delay(user)