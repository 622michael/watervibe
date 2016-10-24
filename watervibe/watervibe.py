from .models import User, Event, Reminder 
import users, reminders
from watervibe_time import now_in_user_timezone, string_for_date, date_for_string
import importlib
from datetime import timedelta
import stats
from events.events import minimum_time_between_event, fringe_time_for_event, minimum_pmf_mean

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

def fitbit_dashboard_alarms (app_id):
	try:
		user = User.objects.get(app_id = app_id, app = "fitbit")
	except:
		return []

	alarms = []

	count = 0
	for reminder in Reminder.objects.filter(user = user):
		if count >= 5:
			break

		date = reminders.date(reminder)

		time_string = date.strftime("%I:%M%p")
		date_string = date.strftime("%m/%d/%Y")

		alarm = (time_string, date_string)
		alarms.append(alarm)
		count += 1

	return alarms


##	Register Sample
## 	-------------------------------------
##	Called when a new sample for an event
##  is added to the users app. If the day
## 	of the week is relavent to the event
## 	the day_of_the_week should be set to
## 	the event's isoweekday.

def register_sample (app, app_id, tag, day_of_the_week = None):

	user = User.objects.filter(app = app,
							   app_id = app_id).first()

	## Clear all the events of that tag
	## Then recreate them from the new data
	events = Event.objects.filter(user = user, tag = tag)
	if day_of_the_week is not None:
		events = events.filter(day_of_week = day_of_the_week)
	for event in events:
		event.is_active = False
		event.save()

	app = importlib.import_module(user.app + "." + user.app)
	event_times = getattr(app, "%s_times" % tag)(app_id, day_of_the_week = day_of_the_week)
	if len(event_times) < 2: 
		return
	if len(event_times[0]) < 2: 
		return

	pmf = stats.event_pmf(event_times, 1440)
	pmf_average = stats.average(pmf)

	if pmf_average < minimum_pmf_mean(tag):
		## All weak probabilities. Only outlier events.
		return

	pmf_variance = stats.variance(pmf, average = pmf_average)
	pmf_std = stats.standard_deviation(pmf, variance = pmf_variance)

	in_event = False
	event_start_minutes = []
	event_end_minutes = []
	event_probabilites = []
	for minute in range(0,1440):
		if pmf[minute] > pmf_average + pmf_variance:
			if in_event is False:
				event_start_minutes.append(minute)
				in_event = True
		else:
			if in_event is True:
				event_end_minutes.append(minute)
				in_event = False


	if len(event_start_minutes) > len(event_end_minutes): ## Assume the last event started at night and ends in the morning
		event_start_minutes[0] = event_start_minutes[len(event_start_minutes) - 1]
		del event_start_minutes[len(event_start_minutes) - 1]

	## If events are too close together, combined them.
	for index in range(0, len(event_end_minutes)):
		if index + 1 >= len(event_start_minutes):
			break

		event_end_time = event_end_minutes[index]
		next_event_start_time = event_start_minutes[index + 1]
		time_between_event = next_event_start_time - event_end_time
		if time_between_event < minimum_time_between_event(tag):
			del event_end_minutes[index]
			del event_start_minutes[index + 1]


	for index in range(0, len(event_start_minutes)):
		start_minute = event_start_minutes[index]
		end_minute = event_end_minutes[index]

		if start_minute < end_minute:
			event_probability_set = pmf[start_minute:end_minute]
		else:
			event_probability_set = pmf[start_minute:1439]
			event_probability_set.extend(pmf[0:end_minute])
		event_average_probablity = stats.average(event_probability_set)
		event_probability_variance = stats.variance(event_probability_set, average = event_average_probablity)

		fringe_start_time = start_minute - fringe_time_for_event(tag)
		if fringe_start_time < 0:
			fringe_start_time = 1440 + fringe_start_time

		fringe_end_time = end_minute + fringe_time_for_event(tag)
		if fringe_end_time > 1440:
			fringe_end_time = fringe_end_time - 1440

		if fringe_end_time > fringe_start_time:
			fringe_pmf = pmf[fringe_start_time:fringe_end_time]
		else:
			fringe_pmf = pmf[fringe_start_time:1439]
			fringe_pmf.extend(pmf[0:fringe_end_time])

		fringe_average_probability = stats.average(fringe_pmf)
		fringe_variance = stats.variance(fringe_pmf, average = fringe_average_probability)

		start_hour = float(start_minute)/60.0
		end_hour = float(end_minute)/60.0

		e = Event.objects.create(user = user,
								 tag = tag,
								 start_time = start_hour, 
								 end_time = end_hour,
								 day_of_week = day_of_the_week,
								 probability = event_average_probablity,
								 probability_variance = event_probability_variance,
								 fringe_probability = fringe_average_probability,
								 fringe_variance = fringe_variance)
		e.save()
