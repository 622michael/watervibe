from fitbit.tests import AppTestClass
import watervibe
from .models import User, Reminder
import reminders, users
from watervibe_time import now_in_user_timezone, seconds_till_reminder
from tasks import sync
from datetime import timedelta


class WaterVibeAppTestClass(AppTestClass): 
	def setUp(self): 
		super(WaterVibeAppTestClass, self).setUp()
		
		self.watervibe_user = user = User.objects.create(app= "fitbit", 
														 app_id= self.user.id, 
														 start_of_period= "08:30-04:00", 
														 end_of_period="20:30-04:00",
														 next_sync_time= "2016-09-19 00:00-04:00", 
														 maximum_reminders = 8
														)

		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								app_id = 1, time = "2016-09-20 08:30-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								app_id = 2, time = "2016-09-20 10:00-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								app_id = 3, time = "2016-09-20 11:30-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								app_id = 4, time = "2016-09-20 13:00-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								time = "2016-09-20 14:30-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								time = "2016-09-20 16:00-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								time = "2016-09-20 17:30-04:00")
		Reminder.objects.create(app= "fitbit", user= self.watervibe_user, 
								time = "2016-09-20 19:00-04:00")

#class WaterVibeTaskTestClass(WaterVibeAppTestClass):
	# def test_sync(self):
	#	sync(self.watervibe_user)
	#	sync(self.watervibe_user)

# class WaterVibeTestClass(AppTestClass):
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

# class RemindersTestClass(AppTestClass):
# 	def setUp(self):
# 		# super(RemindersTestClass, self).setUp()
# 		# watervibe.register_fitbit_user(self.user)
# 		# self.watervibe_user = User.objects.filter(app = "fitbit",
# 		# 										  app_id = self.user.id).first()
		
# 		self.user = User.objects.create(app= "fitbit", app_id= 1, start_of_period= "08:30-04:00", end_of_period="20:30-04:00",
# 		 							next_sync_time = "2016-09-19 00:00-04:00", maximum_reminders = 7)
# 		self.reminder = Reminder.objects.create(app = "fitbit", time = "2016-09-19 14:30-04:00", user = self.user )
# 		Reminder.objects.create(app = "fitbit", time = "2016-09-19 16:30-04:00", user = self.user )
# 		Reminder.objects.create(app = "fitbit", time = "2016-09-19 11:30-04:00", user = self.user )


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
	def test_user_alarms(self): 
		self.assertEqual(8, len(users.user_reminders(self.watervibe_user)))
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
