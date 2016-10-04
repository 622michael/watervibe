import math
from .models import Event
import watervibe_time

## Calculates a weighted average from a set
## The weight is a lambda function of some i
## Where i is the index of x.

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

## OUTDATED: now use event_pmf
def probability(event_tag, at, user = None, day_of_week = None):

	all_events = Event.objects.filter(tag = event_tag)
	
	if user is not None:
		all_events = all_events.filter(user = user)
	if day_of_week is not None:
		all_events = all_events.filter(day_of_week = day_of_week)
	
	total_events = all_events.count()
	count = all_events.filter(start_time__gte = at).filter(end_time__lte = at).count()
	return float(count)/float(total_events)

## A standard variance from a set
## If average is available, it should
## be passed, or it will just be recalculated

def variance(set, average = None, population = True):
	if average is None:
		average = average(set)

	sq_diffrences = [(average - x)**2 for x in set]
	ssd = sum(sq_diffrences)
	if population:
		variance = ssd/len(set)
	else:
		variance = ssd/(len(set) - 1)
	return variance

## A standard deviation from a set
## If average or variance is available it should be
## passed, or they will just be recalculated.

def standard_deviation(set, average = None, population = True, variance = variance):
	if variance is None:
		variance = variance(set, average = average, population = population)

	result = math.sqrt(variance)
	return result

## A standard average from some set of numbers
##
##

def average(set):
	total = sum(set)
	result = float(total)/float(len(set))
	return result


## Not a real pmf, but close. Calculates the
## probability an event is happening at a given time
## by counting all events in the sample that happen
## at that time divide by the number of events in the sample.
## Result_size specifies how large the resulting list is.
## For a bin size of 1 second -> result_size = 86,400
## For a bin size of 1 minute -> result_size = 1440
## For a bin size of 1 hour -> result_size = 24

def event_pmf (event_set, result_size):
	count = [0] * result_size
	second_length_of_bins = float(watervibe_time.seconds_in_a_day)/float(result_size)
	start_times = event_set[0]
	end_times = event_set[1]
	number_of_events = len(start_times)

	for index in range(0, number_of_events):
		start_datetime = watervibe_time.date_for_string(start_times[index])
		end_datetime = watervibe_time.date_for_string(end_times[index])
		event_length = (end_datetime - start_datetime).total_seconds()

		start_time = start_datetime.hour * 3600 + start_datetime.minute * 60
		in_bin = int(start_time/second_length_of_bins)
		time_in_event = 0

		while time_in_event < event_length:
			count[in_bin] = count[in_bin] + 1
			in_bin = in_bin + 1
			if in_bin >= len(count):
				in_bin = 0

			time_in_event += second_length_of_bins

	result = [float(x)/float(number_of_events) for x in count]
	return result