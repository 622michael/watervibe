## This class links the abstarct event classes (stored in events/*.py)
## to the rest of the app. Also handles any tasks related to events that
## require some calculations like duration.

import importlib
from watervibe.models import Event

## Returns the given event duration
## in minutes.
def duration(event):
	if event.start_time > event.end_time:
		minutes = (24 - event.start_time)*60
		minutes = minutes + event.end_time * 60
	else:
		length = event.end_time - event.start_time
		minutes = length * 60

	return minutes

##	Minimum PMF mean
## 	-------------------------------------
## 	Returns the minimum PMF value that an
##	event must have in order for it to be
##  a vaild pmf.

def minimum_pmf_mean(tag):
	event_abstract = importlib.import_module("watervibe.events." + tag)
	print event_abstract
	return event_abstract.minimum_pmf_mean

##	Minimum Time Between Event
## 	-------------------------------------
## 	Sets the frequency at which an event
##  can occur. Useful in making sure duplicate
##  events do not occur.

def minimum_time_between_event(tag):
	event_abstract = importlib.import_module("watervibe.events." + tag)
	return event_abstract.minimum_time_between_event


## Fringe time for event
## -------------------------------------
## A time buffer to insure the "safety" of
## events.

def fringe_time_for_event(tag):
	event_abstract = importlib.import_module("watervibe.events." + tag)
	return event_abstract.fringe_time_for_event

## Adjust Reminder At
## -------------------------------------
## Returns the proper time for the reminder
## That is set to occur during an event.

def adjust_reminder_at(reminder_time, event):
	event_abstract = importlib.import_module("watervibe.events." + event.tag)
	return event_abstract.adjust_reminder_at(reminder_time, event)

## This insures that there is an active
## sleep event on every day of the week.
## If there is not one is set for 8:30pm - 8:30am
def validate_user_sleeps(user):
	for day in range(0,8):
			sleep_events = Event.objects.filter(user = user, day_of_week = day, is_active = 1, tag = "sleep")
			if len(sleep_events) == 0: 
				default_sleep_event = Event.objects.filter(user = user, day_of_week = day, tag = "sleep", start_time = 20.5, end_time = 8.5).first()

				if default_sleep_event is None: 
					default_sleep_event = Event.objects.create(user = user, day_of_week = day, tag = "sleep", start_time = 20.5, end_time = 8.5, is_active = 1)