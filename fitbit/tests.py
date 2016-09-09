from django.test import TestCase
from . import fitbit
from .models import User, Device

# Create your tests here.
class FitBitTestClass(TestCase):
	def setUp(self):
		self.user = User.objects.create( fitbit_id="4TP97K", 
								access_token="eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0VFA5N0siLCJhdWQiOiIyMjdSUjkiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd3BybyB3c2xlIHd3ZWkgd2FjdCB3c2V0IHdsb2MiLCJleHAiOjE0NzM0MjY5ODEsImlhdCI6MTQ3MzM5ODE4MX0.xfFi0x4lV3nT2S5zJiKtX66jQ1pKNtA6P6hhp8c8CQI", 
								scope="activity heartrate profile location sleep weight settings", 
								refresh_token="d48586e5bf9ca6ddf1eb45e511cfbc51fd3c2dbed050ae92c1e73af43396dc94")
		self.device = Device.objects.create(fitbit_id = "310104047",
										version = "Charge HR",
										device_type = "TRACKER",
										user = self.user)

	def test_other_thing(self):
		devices = Device.objects.filter(user=self.user.id)
		print devices.first().version


	def test_requesting_user_id(self):
		user = User.objects.first()
		self.assertEqual(self.user.id, 1)

	def test_devices_for_user(self):
		user = User.objects.first()
		devices = fitbit.devices_for_user(self.user)
		self.assertEqual(len(devices), 1)
