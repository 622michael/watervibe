### Watervibe reminders:
## Handles the reminders 
## 
##
##
import users
import watervibe_time
# from watervibe_time import date_for_string, string_for_datepyth
from models import Reminder, Time
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
	time_between_reminders = users.maximum_time_between_reminders(user, start_of_period)
	last_distance = 0
	
	print "Setting reminders every %d seconds" % time_between_reminders.total_seconds()
	print "Set to drink %d ounces this period" % ounces_drunk_in_period
	print "Required to drink %d ounces" % required_ounces

	while ounces_drunk_in_period < required_ounces:
		next_reminder_date = last_reminder_date + time_between_reminders
		
		if next_reminder_date < watervibe_time.now_in_user_timezone(user):
			next_reminder_date = watervibe_time.now_in_user_timezone(user) + timedelta(minutes = 5)
			print "Trying ot set one before another"		
		
		event_reminder = 0
		time = Time.objects.filter(hour = next_reminder_date.hour, minute = next_reminder_date.minute).first()
		asleep_possibility = stats.probability("sleep", time, user = user, day_of_week = next_reminder_date.isoweekday())
		if asleep_possibility > 0.25:
			print "Sleeping at %02d:%02d" % (time.hour, time.minute)
			length = 0
			while asleep_possibility > 0.25:
				length += 1
				next_reminder_date = next_reminder_date + timedelta(minutes = length)
				time = Time.objects.filter(hour = next_reminder_date.hour, minute = next_reminder_date.minute).first()
				asleep_possibility = stats.probability("sleep", time, user = user, day_of_week = next_reminder_date.isoweekday())
			print "End sleep at %02d:%02d" % (time.hour, time.minute)
			next_reminder_date = next_reminder_date + timedelta(hours = 1) # If I wasn't lazy this woudl be th variance of the event
				
	
		last_reminder = create_reminder(next_reminder_date, user)
		if(next_reminder_date > end_of_period):
			break
				
		last_reminder_date = next_reminder_date
		ounces_drunk_in_period = users.ounces_to_drink_in_period(user, start_of_period, end_of_period)
		print ounces_drunk_in_period
