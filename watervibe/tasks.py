## Watervibe app tasks:
## A clerey delegator. 
##
##
##

from models import User
import users, reminders
import importlib
from .celery import app
from watervibe_time import date_for_string, seconds_till_sync, seconds_till_update
from datetime import datetime

@app.task(ignore_result = True)
def setup(user):
	update(user)
	sync(user)

@app.task(ignore_result = True)
def update(user):
	users.calculate_stats(user)
	reminders.create_reminders_for_user(user)

	update.apply_async(args= [user], countdown=seconds_till_update(user))

@app.task(ignore_result = True)
def sync(user):
	app = importlib.import_module(user.app + "." + user.app)

	for reminder in users.reminders(user):
		if reminder.app_id is None:
			alarm_app_id = app.set_alarm(user.app_id, date_for_string(reminder.time))
			if alarm_app_id is None:
				return

			reminder.app_id = alarm_app_id
			reminder.save()

	sync.apply_async(args= [user], countdown=seconds_till_sync(user))