from .models import User
from tasks import setup
import users, reminders
from watervibe_time import now_in_user_timezone, string_for_date
import importlib

def setup(user):
	users.calculate_stats(user)
	reminders.create_reminders_for_user(user)
	sync(user)

def sync(user): 
	app = importlib.import_module(user.app + "." + user.app)

	for reminder in users.user_reminders(user):
		if reminder.app_id is None:
			alarm_app_id = app.set_alarm(user.app_id, reminders.date(reminder))
			reminder.app_id = alarm_app_id
			reminder.save()

	user.last_sync = string_for_date(now_in_user_timezone(user))
	user.next_sync_time = users.calculate_sync_time(user)
	user.save()

def register_fitbit_user(fitbit_user):
	try:
		user = User.objects.get(app_id = user_id)
	except:
		user = User.objects.create(app = 'fitbit',
							   app_id = fitbit_user.id
							  )
	 	user.save()
	 	setup(user)