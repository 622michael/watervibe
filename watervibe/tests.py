from fitbit.tests import AppTestClass
import watervibe
from .models import User, Reminder, Time
import reminders, users
from watervibe_time import now_in_user_timezone, seconds_till_reminder, date_for_string
from tasks import sync
from datetime import timedelta, datetime
import fitbit.users


class WaterVibeAppTestClass(AppTestClass): 
	def setUp(self): 
		super(WaterVibeAppTestClass, self).setUp()
		
		self.watervibe_user = User.objects.create(app = "fitbit", 
												  app_id = self.user.id, 
												  start_of_period = "08:30-04:00", 
												  end_of_period = "20:30-04:00",
												  next_sync_time = "2016-09-19 00:00-04:00", 
												  maximum_reminders = 8)

		for hour in range(0, 24):
			for minute in range (0, 60):
				t = Time.objects.create(hour = hour, minute = minute)
				t.save

		fitbit.users.sync_sleep_logs(self.user)


#class WaterVibeTaskTestClass(WaterVibeAppTestClass):
	# def test_sync(self):
	#	sync(self.watervibe_user)
	#	sync(self.watervibe_user)

# class WaterVibeTestClass(AppTestClass):
	# def test_register_event(self):
	# 	start_time = "2016-09-11 07:44-04:00"
	# 	end_time = "2016-09-11 13:22-04:00"

	# 	watervibe.register_event("fitbit", self.user.id, "sleep", 
	# 		date_for_string(start_time), date_for_string(end_time))


# 	def test_setup(self):
# 		watervibe.register_fitbit_user(self.user)

# 		try:
# 			user = User.objects.filter(app_id = self.user.id)

# 			self.assertEqual('08:30-04:00', user.start_of_period)
# 			self.assertEqual('20:30-04:00', user.end_of_period)
# 			self.assertEqual(64.0, user.ounces_in_a_day)
# 			self.assertEqual(8.0, user.drink_size)
# 		except:
# 			assert("NoUser")

# 	def test_sync(self):
# 		user = User.objects.create(app= "fitbit", app_id= 1, start_of_period= "08:30-04:00", end_of_period="20:30-04:00",
# 									next_sync_time= "2016-09-19 00:00-04:00", maximum_reminders = 7)
# 		reminder = Reminder.objects.create(app = "fitbit", time = "2016-09-18 11:30-04:00", user_id= 1)
# 		sync(user)
# 		self.assertEqual(reminder.app_id, 1)

class RemindersTestClass(WaterVibeAppTestClass):
	def test_create_reminders_for_user(self):
		reminders.create_reminders_for_user(self.watervibe_user)


# 	def test_next_reminder_for(self):
# 		reminder = reminders.next_reminder_for(self.user)
# 		self.assertEqual(reminder.time, "2016-09-19 14:30-04:00")

# 	def test_time_till_sync(self):
# 		print "Seconds till: %d" % seconds_till_reminder(self.reminder)

# 	def test_create_reminder(self):
# 		time = now_in_user_timezone(self.user) + timedelta(seconds= 10)
# 		reminders.create_reminder(time, self.user)
# 		time = now_in_user_timezone(self.user) + timedelta(seconds= 20)
# 		reminders.create_reminder(time, self.user)






class UsersTestClass(WaterVibeAppTestClass):
	def test_maximum_time_between_reminders (self):
		max_time = users.maximum_time_between_reminders(self.watervibe_user, datetime.now())
		self.assertEqual(max_time, timedelta(seconds = 3842.194193))

	def test_calculate_sync_time(self):
		next_sync_time = users.sync_time(self.watervibe_user)
		self.assertEqual(next_sync_time, "2016-09-28 09:00-04:00")

	# def test_user_alarms(self): 
	# 	self.assertEqual(8, len(users.user_reminders(self.watervibe_user)))
# 	def setUp(self):
# 		self.watervibe_user = User.objects.create(app= 'fitbit', app_id=1, start_of_period = "08:30-04:00")

# 	def test_user_timezone(self):
# 		print users.user_timezone(self.watervibe_user)

# 	def test_user_now(self):
# 		print now_in_user_timezone(self.watervibe_user)

# 	def test_calculate_stats(self):
# 		users.calculate_stats(self.watervibe_user)

# 		self.assertEqual('08:30-04:00', self.watervibe_user.start_of_period)
# 		self.assertEqual('20:30-04:00', self.watervibe_user.end_of_period)
# 		self.assertEqual(64.0, self.watervibe_user.ounces_in_a_day)
# 		self.assertEqual(8.0, self.watervibe_user.drink_size)
