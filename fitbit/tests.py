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
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd3NldCB3YWN0IHdsb2MiLCJleHAiOjE0NzU0NDA2ODAsImlhdCI6MTQ3NTQxMTg4MH0.L8AwcuJBCR54BdeEcZMJQVZpd1qHyytTJXRbLv_pl4A", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="4e8ab05646fdb1d0b15b931ecc89647381e4dab301074a1b5da0642bd1e91cf2",
								access_token_expiration = "2016-09-25 12:00+00:00")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

		
		users.update_profile(self.user)

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
