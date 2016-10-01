import math
from .models import Event, Time
from watervibe_time import date_for_string, now_in_user_timezone


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


def probability(event_tag, at, user = None):
	if user is not None:
		total_events = (now_in_user_timezone(user) - date_for_string(user.beginning_sample_date)).days * 1440
		count = Event.objects.filter(tag = event_tag, time = at, user = user)

	return count/total_events