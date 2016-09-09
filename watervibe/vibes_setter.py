from datetime import timedelta
from . import user_manager
from .models import Reminder
import math
import fitbit.fitbit

def add_vibes_for_next_period_for_user(user):
	

	start_of_period = user.start_of_period
	end_of_period = user.end_of_period

	if start_of_period is None or end_of_period is None:
		start_of_period, end_of_period = user_manager.period_for_user(user)

	period_length = user.end_of_period - user.start_of_period

	required_ounces = user.ounces_in_a_period
	drink_size = user.drink_size
	number_of_reminders = math.ceil(required_ounces/drink_size)
	print number_of_reminders

	for reminder_index in range(0, int(number_of_reminders)):
		time = start_of_period + timedelta(seconds=reminder_index*(period_length.seconds/number_of_reminders))
		reminder = Reminder.objects.create(time = time)

		devices = fitbit.fitbit.devices_for_user(user)
		try:
			for device in devices:
				alarms.set_alarm_for(user, device, time)
		except:
			# Called when there are no devices
			# @update load user's devices
			
			print "No Devices"
			return