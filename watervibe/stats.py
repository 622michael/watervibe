import math
from .models import Event, Time


def weighted_average(data_set, weight):
	total = 0.0
	count = 0.0
	for i in range(0, len(data_set)):
		x = data_set[i]
		total += x*weight(i)
		count += 1
	if count != 0:
		return total/count
	else:
		return 0


def probability(event_tag, at, user = None, day_of_week = None):
	all_events = Event.objects.filter(tag = event_tag)
	
	if user is not None:
		all_events = all_events.filter(user = user)
	if day_of_week is not None:
		all_events = Event.objects.filter(day_of_week = day_of_week)
	
	count = all_events.filter(times = at).count()
	total_events = all_events.count()
	return float(count)/float(total_events)
