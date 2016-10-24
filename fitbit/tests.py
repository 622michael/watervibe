from django.test import TestCase
from . import fitbit
from .models import User, Device, Alarm, Sleep
import dateutil.parser
import authorization
import alarms
import users
from fitbit_time import now, string_for_date
from datetime import timedelta

# Create your tests here.
class AppTestClass(TestCase):
	def setUp(self):
		self.user = User.objects.create( fitbit_id="4TP97K", 
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd3NldCB3YWN0IHdsb2MiLCJleHAiOjE0NzU3NTU1MDIsImlhdCI6MTQ3NTcyNjcwMn0.HwEyw2lzqO2Qk5PDGLKBp7SdIAcG1dyjB0SWdUgn41k", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="65739a29c12bc74ba563bac4c24cf49e9942389cac7d5376f371184243d2ca87",
								access_token_expiration = "2016-09-25 12:00+00:00")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)


		Sleep.objects.create(fitbit_id = "12613384968",
									 is_main_sleep = 1,
									start_time = "2016-09-22 06:23-04:00",
									end_time = "2016-09-22 07:56-04:00",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12626120836",
									 is_main_sleep = 1,
									start_time = "2016-09-24 03:42-04:00",
									end_time = "2016-09-24 08:06-04:00",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12628859393",
									 is_main_sleep = 1,
									start_time = "2016-09-25 02:03-04:00",
									end_time = "2016-09-25 08:02-04:00",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12642373013",
									 is_main_sleep = 1,
									start_time = "2016-09-25 15:28-04:00",
									end_time = "2016-09-25 18:17-04:00",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12660782864",
									 is_main_sleep = 1,
									start_time = "2016-09-26 02:36-04:00",
									end_time = "2016-09-26 06:56-04:00",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12669899859",
									 is_main_sleep = 1,
									start_time = "2016-09-28 00:38-04:00",
									end_time = "2016-09-27 08:24-04:00 ",
									duration = 5580000,
									user = self.user)
		Sleep.objects.create(fitbit_id = "12682157426",
									 is_main_sleep = 1,
									start_time = "2016-09-28 23:40-04:00",
									end_time = "2016-09-28 07:26-04:00",
									duration = 5580000,
									user = self.user)
		
		# users.update_profile(self.user)
 
		# Alarm.objects.create(time = "2016-09-27 14:30-04:00", 
		# 	fitbit_id = "336601763", 
		# 	user = self.user,
		# 	device = self.device)

		# Alarm.objects.create(time = "2016-09-27 16:00-04:00", 
		# 	fitbit_id = "336692478", 
		# 	user = self.user,
		# 	device = self.device)

		# Alarm.objects.create(time = "2016-09-27 17:30-04:00", 
		# 	fitbit_id = "336617891", 
		# 	user = self.user,
		# 	device = self.device)

		# Alarm.objects.create(time = "2016-09-27 19:00-04:00", 
		# 	fitbit_id = "336607812", 
		# 	user = self.user,
		# 	device = self.device)

class UserTestClass(AppTestClass):
	def test_update_profile(self):
		users.update_profile(self.user)
		self.assertEqual(self.user.weight, 134.92290445416)


	def test_sleep_log (self): 
		date = string_for_date(now() - timedelta(days = 1))
		print "[****START TEST SLEEP LOG %s****]" %  date
		log  = users.sleep_log(self.user, now() - timedelta(days = 1))
		print "[****START TEST SLEEP LOG %s****]" % date

		print log

	def test_sync_sleep_logs (self): 
		users.sync_sleep_logs(self.user)

		self.assertTrue(len(Sleep.objects.filter(user_id = self.user.id)) != 0)



# class FitBitTestClass(AppTestClass):
# 	def test_devices_for_user(self):
# 		devices = fitbit.devices_for_user(self.user)
		
# 		self.assertEqual(len(devices), 1)

# 	def test_set_alarm_for_user(self):
# 		time_string = "2016-09-16 12:10-04:00"
# 		date = dateutil.parser.parse(time_string)
# 		m = fitbit.set_alarm (self.user.id, date)
# 		self.assertEqual(m, 1)


class AlarmTestClass(AppTestClass):

	# def test_clear_used_alarms_on_device(self):
	# 	r = alarms.clear_used_alarms_on_device(self.user, self.device)
	# 	self.assertTrue(r)

	def test_user_alarms(self):
		self.assertEqual(8, alarms.user_alarms_count(self.user))



class AuthorizationTestClass(AppTestClass):
	def test_refresh_access_code_for_user(self):
		print "Test is off"
	# 	old_access_token = self.user.access_token
	# 	authorization.refresh_access_for_user(self.user)
	# 	current_access_token = self.user.access_token

	# 	self.assertTrue(old_access_token != current_access_token)
