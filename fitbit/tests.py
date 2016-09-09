from django.test import TestCase
from . import fitbit
from .models import User, Device
import dateutil.parser

# Create your tests here.
class FitBitTestClass(TestCase):
	def setUp(self):
		self.user = User.objects.create( fitbit_id="4TP97K", 
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzM0NjA2NjgsImlhdCI6MTQ3MzQzMTg2OH0.cYD9lWlhU8mp6XZIBSuYIucdBDuoPIgMsEG6ZunzTU8", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="b95163e93e8ce7924d77e1f660878deb6f6d5d8bb631cc94832e1aa05daeb34a")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

	def test_devices_for_user(self):
		devices = fitbit.devices_for_user(self.user)
		self.assertEqual(len(devices), 1)

	def test_set_alaram_for_user(self):
		time_string = "12:10-04:00"
		date = dateutil.parser.parse(time_string)
		fitbit.set_alarm_for_user_device_time(self.user, self.device, date)

