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
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd3NldCB3YWN0IHdsb2MiLCJleHAiOjE0NzQyMzY1NDUsImlhdCI6MTQ3NDIwNzc0NX0.gd5wi7tzLefN3gnPKVMW8MqoLcO0MjHRDSLPAe6Oa78", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="c55925bcf38da16825c46b4c3f3bd1b8d1c94088e41a1adc38776055f8e1dc21",
								access_token_expiration = "2016-09-16 12:00+00:00")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

		Alarm.objects.create(time = "2016-09-10 08:30-04:00", 
			fitbit_id = "329995322", 
			user = self.user,
			device = self.device)


class FitBitTestClass(AppTestClass):
	def test_devices_for_user(self):
		devices = fitbit.devices_for_user(self.user)
		
		self.assertEqual(len(devices), 1)

	def test_set_alarm_for_user(self):
		time_string = "2016-09-16 12:10-04:00"
		date = dateutil.parser.parse(time_string)
		m = fitbit.set_alarm (self.user.id, date)
		self.assertEqual(m, 1)


class AlarmTestClass(AppTestClass):

	def test_clear_used_alarms_on_device(self):
		r = alarms.clear_used_alarms_on_device(self.user, self.device)
		self.assertTrue(r)

	def test_user_alarms(self):
		self.assertEqual(8, alarms.user_alarms(self.user))



class AuthorizationTestClass(AppTestClass):
	def test_refresh_access_code_for_user(self):
		print "Test is off"
	# 	old_access_token = self.user.access_token
	# 	authorization.refresh_access_for_user(self.user)
	# 	current_access_token = self.user.access_token

	# 	self.assertTrue(old_access_token != current_access_token)
