## Watervibe app tasks:
## A clerey delegator. 
##
##
##

import users, reminders
from .celery import app
from watervibe_time import date_for_string, seconds_till_sync
from datetime import datetime

@app.task(ignore_result = True)
def setup(user):
	update(user)
	sync.apply_async(args= [user], countdown=seconds_till_sync(user))

@app.task(ignore_result = True)
def update(user):
	users.calculate_stats(user)
	reminders.create_reminders_for_user(user)

	update.apply_async(args= [user], countdown=seconds_till_update(user))

@app.task(ignore_result = True)
def sync(user):
	for reminder in user.reminders():
		if reminder.app_id is None:
			fitbit.fitbit.set_alarm (user.fitbit_user, reminder.time)

	sync.apply_async(args= [user], countdown=seconds_till_sync(user))