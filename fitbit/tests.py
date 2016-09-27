from django.test import TestCase
from . import fitbit
from .models import User, Device, Alarm
import dateutil.parser
import authorization
import alarms
import users

# Create your tests here.
class AppTestClass(TestCase):
	def setUp(self):
		self.user = User.objects.create( fitbit_id="4TP97K", 
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzUwMjAxNzcsImlhdCI6MTQ3NDk5MTM3N30.6Ft6ytXekIHU_4PsUjhm7SUTYuH8oS-fxqaAXRO2nHU", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="e6188a45d20779cb8c4c4ae0b62c4dfb590823d40f1f5c86a5f6c5f1add9ece8",
								access_token_expiration = "2016-09-25 12:00+00:00")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

		users.update_profile(self.user)

		Alarm.objects.create(time = "2016-09-27 14:30-04:00", 
			fitbit_id = "336601763", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-27 16:00-04:00", 
			fitbit_id = "336692478", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-27 17:30-04:00", 
			fitbit_id = "336617891", 
			user = self.user,
			device = self.device)

		Alarm.objects.create(time = "2016-09-27 19:00-04:00", 
			fitbit_id = "336607812", 
			user = self.user,
			device = self.device)

class UserTestClass(AppTestClass):
	def test_update_profile(self):
		users.update_profile(self.user)
		self.assertEqual(self.user.weight, 134.92290445416)



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
