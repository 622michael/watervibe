## Watervibe app tasks:
## A clerey delegator. 
##
##
##

from models import User
import users, reminders
import importlib
from .celery import app
from watervibe_time import date_for_string, seconds_till_sync, seconds_till_update, string_for_date, now_in_user_timezone
from datetime import datetime, timedelta

@app.task(ignore_result = True)
def setup(user):
	update(user)
	sync(user)

@app.task(ignore_result = True)
def update(user):
	if user.last_update is not None:
		if date_for_string(user.last_update) - now_in_user_timezone(user) < timedelta(seconds=30):
			print "Extra Celery Process. Ignoring."
			return 

	users.calculate_stats(user)
	reminders.create_reminders_for_user(user)

	user.last_update = string_for_date(now_in_user_timezone(user))
	user.save()

@app.task(ignore_result = True)
def sync(user):
	print "Next sync time: " + user.next_sync_time
	if user.last_sync is not None:
		print "Sync previously..."
		if date_for_string(user.last_sync) - now_in_user_timezone(user) < timedelta(seconds=30):
			print "Extra Celery Process. Ignoring."
			return 

	app = importlib.import_module(user.app + "." + user.app)

	for reminder in users.reminders(user):
		if reminder.app_id is None:
			alarm_app_id = app.set_alarm(user.app_id, date_for_string(reminder.time))
			reminder.app_id = alarm_app_id
			reminder.save()

	user.last_sync = string_for_date(now_in_user_timezone(user))
	user.next_sync_time = users.calculate_sync_time(user)
	user.save()

	sync.apply_async(args= [user], countdown=seconds_till_sync(user))