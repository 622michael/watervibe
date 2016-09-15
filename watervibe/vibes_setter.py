from datetime import timedelta
from . import users
from .models import Reminder
import math
import fitbit.fitbit

def add_vibes_for_next_period_for_user(user):
	
	start_of_period, end_of_period = users.period_for_user(user)

	period_length = start_of_period - end_of_period

	required_ounces = user.ounces_in_a_period
	drink_size = user.drink_size
	number_of_reminders = math.ceil(required_ounces/drink_size)
	print number_of_reminders

	for reminder_index in range(0, int(number_of_reminders)):
		print "Creating alarm..."
		reminder_datetime = start_of_period + timedelta(seconds=reminder_index*(period_length.seconds/number_of_reminders))
		reminder = Reminder.objects.create(time = reminder_datetime)

		devices = fitbit.fitbit.devices_for_user(user)
		for device in devices:
			fitbit.fitbit.set_alarm_for_user_device_time(user, device, reminder_datetime)