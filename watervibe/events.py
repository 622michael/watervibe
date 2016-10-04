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


def minimum_time_between_event(tag):
	if tag == "sleep":
		return 60

	return 0

def fringe_time_for_event(tag):
	if tag == "sleep":
		return 60

	return 0

## Returns the proper time for the reminder
## That is set to occur during an event.
def adjust_reminder_at(reminder_time, event):
	if event.tag == "sleep":
		print "is sleeping..."
		return event.end_time + 1

	return reminder_time