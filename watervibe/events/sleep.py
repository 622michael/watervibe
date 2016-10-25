## Stores all information needed to understand
## and process a sleep event. Units are in minutes.

## --- reminder_interaction
## Sets when the event is "viewed" by watervibes.
## An interruptive event is seen when trying to set
## an alarm during the event.
## An additive event is seen when setting reminders
## and when calculating how much water should be drank.

reminder_interaction = "interruptive"

## --- minimum_pfm_mean
## The value that a pmf must pass so
## that it acutally counts as a pattern
## being established.

minimum_pmf_mean = 0.2

## --- minimum_time_between_event
## Sets the frequency at which an event
## can occur.
##

minimum_time_between_event = 60

## --- fringe_time_for_event
## A time buffer around the event in minutes.
## Accounts for the probability the event occurs
## earlier or later than the actual event.
## For example, setting an alarm whenever a user is
## a sleep is just bad desin. This increases the probabilty
## that that doesn't happen. 

fringe_time_for_event = 60

## Returns the proper time for the reminder
## That is set to occur during an event.
def adjust_reminder_at(reminder_time, event):
	if event.is_active:
		new_reminder_time = event.end_time + fringe_time_for_event/60.0
		if new_reminder_time > 23:
			new_reminder_time = new_reminder_time - 23

		return new_reminder_time
	else:
		return event.end_time