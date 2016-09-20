from django.test import TestCase
from . import fitbit
from .models import User, Device, Alarm
import dateutil.parser
import authorization
import alarms

# Create your tests here.
class AppTestClass(TestCase):
	def setUp(self):
		self.user = User.objects.create( fitbit_id="4TP97K", 
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzQ0MTMzMTUsImlhdCI6MTQ3NDM4NDUxNX0.gd5xixultslwm8lpogzGaNtj96ruuSwUYc2felJfL-E", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="2cc2a5ef8b08783011ea9d5d05c876ef663104c8c76f28b1df4b5800774e2526",
								access_token_expiration = "2016-09-25 12:00+00:00")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

		Alarm.objects.create(time = "2016-09-20 08:30-04:00", 
			fitbit_id = "333622106", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-20 10:00-04:00", 
			fitbit_id = "333644281", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-20 11:30-04:00", 
			fitbit_id = "333646297", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-20 13:00-04:00", 
			fitbit_id = "333626138", 
			user = self.user,
			device = self.device)


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
