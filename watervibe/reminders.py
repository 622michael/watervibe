### Watervibe reminders:
## Handles the reminders 
## 
##
##
import users
import watervibe_time
# from watervibe_time import date_for_string, string_for_datepyth
from .models import Reminder, Time
from datetime import timedelta
import stats

def date(reminder):
	return watervibe_time.date_for_string(reminder.time)


def reminders_available_at_next_sync(user):
	reminders = Reminder.objects.filter(user = user.id).order_by('-time')
	available_spots =  users.maximum_reminders(user)
	next_sync_time = watervibe_time.date_for_string(user.next_sync_time)
	for reminder in reminders:
		if watervibe_time.date_for_string(reminder.time) > next_sync_time:
			available_spots = available_spots - 1
		else:
			break

	return available_spots

def create_reminder(time, user):
	print "Adding reminder at " + watervibe_time.string_for_date(time)
	reminder = Reminder.objects.create(time= watervibe_time.string_for_date(time),
							user= user)
	reminder.save()
	return reminder

def next_reminder_for(user): 
	reminders = users.user_reminders(user)
	now = watervibe_time.now_in_user_timezone(user)
	for reminder in reminders:
		reminder_date = watervibe_time.date_for_string(reminder.time)
		if now < reminder_date:
			return reminder

	return None


def last_reminder_for_user(user):
	return Reminder.objects.filter(user = user.id).last()

def time_between_reminders_for_user(user):
	return timedelta(hours = 1, minutes = 30)

def reminder_count(user):
	return Reminder.objects.filter(user = user.id).count()

## Adds 24 hours of reminders to the database
## Starts at the last reminder.
##
def create_reminders_for_user (user):
	last_reminder = last_reminder_for_user(user)

	if last_reminder is None: 
		soon = watervibe_time.now_in_user_timezone(user) + timedelta(minutes = 30)
		last_reminder = create_reminder(soon, user) 

	last_reminder_date = watervibe_time.date_for_string(last_reminder.time)
	hour = last_reminder_date.hour
	minute = last_reminder_date.minute

	start_of_period = last_reminder_date
	end_of_period = last_reminder_date + timedelta(days = 1)
	ounces_drunk_in_period = users.ounces_to_drink_in_period(user, start_of_period, end_of_period)
	required_ounces = users.ounces_in_period(user, start_of_period, end_of_period)
	time_between_reminders = time_between_reminders_for_user(user)
	last_distance = 0
	while ounces_drunk_in_period < required_ounces:
		next_reminder_date = last_reminder_date + time_between_reminders - timedelta(minutes = last_distance)

		time = Time.objects.filter(hour = next_reminder_date.hour, minute = next_reminder_date.minute)
		asleep_possibility = stats.probability("sleep", time, user = user, day_of_week = next_reminder_date.isoweekday())
		if asleep_possibility > 0.25:
			distance_before = None
			distance_after = None
			distance = 0

			while distance_before is None or distance_after is None:
				distance += 1
				datetime_before = next_reminder_date - timedelta(minutes = distance)
				if datetime_before < start_of_period:
					datetime_before = -1

				datetime_after = next_reminder_date + timedelta(minutes = distance)
				if datetime_after > end_of_period:
					datetime_after = -1

				if distance_before is None:
					possible_time = Time.objects.filter(hour = datetime_before.hour, minute = datetime_before.minute)
					asleep_possibility = stats.probability("sleep", time, user = user, day_of_week = distance_before.isoweekday())
					if asleep_possibility < 0.25:
						distance_before = distance

				if distance_after is None:
					possible_time = Time.objects.filter(hour = datetime_after.hour, minute = datetime_before.minute)
					asleep_possibility = stats.probability("sleep", time, user = user, day_of_week = distance_before.isoweekday())
					if asleep_possibility < 0.25:
						distance_after = distance

			if distance_before < 0 and distance_after < 0:
				break
			elif distance_before < 0:
				next_reminder_date = last_reminder_date - timedelta(minutes = distance_before)
				last_distance = -1 * distance_before
			elif distance_after < 0:
				next_reminder_date = last_reminder_date + timedelta(minutes = distance_after)
				last_distance = distance_after
			elif distance_after < distance_before:
				next_reminder_date = last_reminder_date + timedelta(minutes = distance_after)
				last_distance = distance_after
			elif distance_before < distance_after:
				next_reminder_date = last_reminder_date - timedelta(minutes = distance_before)
				last_distance = -1 * distance_before

		create_reminder(next_reminder_date, user)
		ounces_drunk_in_period = users.ounces_in_period(user, watervibe_time.string_for_date(start_of_period), watervibe_time.string_for_date(end_of_period))