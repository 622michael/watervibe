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
		time_since_last_update = date_for_string(user.last_sync) - now_in_user_timezone(user)
		if abs(time_since_last_sync.total_seconds()) < abs(timedelta(minutes=60).total_seconds()):
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
		time_since_last_sync = date_for_string(user.last_sync) - now_in_user_timezone(user)
		if  abs(time_since_last_sync.total_seconds()) < abs(timedelta(minutes=60).total_seconds()):
			print "Extra Celery Process. Last Synced: %d seconds ago." % time_since_last_sync.total_seconds()
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