from .models import User, Event, Time
from tasks import setup
import users, reminders
from watervibe_time import now_in_user_timezone, string_for_date, date_for_string
import importlib

def setup(user):
	users.calculate_stats(user)
	reminders.create_reminders_for_user(user)
	sync(user)

def sync(user): 
	app = importlib.import_module(user.app + "." + user.app)

	for reminder in users.user_reminders(user):
		if reminder.app_id is None:
			if reminders.date(reminder) > now_in_user_timezone(user):
				alarm_app_id = app.set_alarm(user.app_id, reminders.date(reminder))
				reminder.app_id = alarm_app_id
				reminder.save()
				if alarm_app_id is None:
					break

	user.last_sync = string_for_date(now_in_user_timezone(user))
	user.next_sync_time = users.sync_time(user)
	user.save()

def register_fitbit_user(fitbit_user):
	try:
		user = User.objects.get(app_id = fitbit_user.id)
	except:
		user = User.objects.create(app = 'fitbit',
							  	   app_id = fitbit_user.id)
	 	user.save()
	 	setup(user)

##	Adds an event to the timeline
##	Dates must be datetime objects
## 
def register_event(app, app_id, tag, start_date, end_date):
	user = User.objects.filter(app = app, 
								 app_id = app_id).first()

	event = Event.objects.create(user = user,
								   start_date = string_for_date(start_date),
								   end_date = string_for_date(end_date),
								   tag = tag,
								   day_of_week = start_date.isoweekday())

	event_length = int((end_date - start_date).total_seconds()/60)
	for minute in range(0, event_length + 1):
		time_date = start_date + timedelta(minute = x)

		time = Time.objects.filter(hour = time_date.hour, minute = time_date.minute).first()
		event.times.add(time)

	event.save()

	if start_date < date_for_string(user.beginning_sample_date):
		user.beginning_sample_date = event.start_date
		user.save()