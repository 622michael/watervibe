from fitbit.tests import AppTestClass
import watervibe
from .models import User
import reminders, users
from watervibe_time import now_in_user_timezone

class WaterVibeTestClass(AppTestClass):
	def test_setup(self):
		watervibe.register_fitbit_user(self.user)

		try:
			user = User.objects.filter(app_id = self.user.id)

			self.assertEqual('08:30-04:00', user.start_of_period)
			self.assertEqual('20:30-04:00', user.end_of_period)
			self.assertEqual(64.0, user.ounces_in_a_day)
			self.assertEqual(8.0, user.drink_size)
		except:
			assert("NoUser")

class RemindersTestClass(AppTestClass):
	def setUp(self):
		super(RemindersTestClass, self).setUp()
		watervibe.register_fitbit_user(self.user)
		self.watervibe_user = User.objects.filter(app = "fitbit",
												  app_id = self.user.id).first()



class UsersTestClass(AppTestClass):
	def setUp(self):
		self.watervibe_user = User.objects.create(app= 'fitbit', app_id=1, start_of_period = "08:30-04:00")

	def test_user_timezone(self):
		print users.user_timezone(self.watervibe_user)

	def test_user_now(self):
		print now_in_user_timezone(self.watervibe_user)

	def test_calculate_stats(self):
		users.calculate_stats(self.watervibe_user)

		self.assertEqual('08:30-04:00', self.watervibe_user.start_of_period)
		self.assertEqual('20:30-04:00', self.watervibe_user.end_of_period)
		self.assertEqual(64.0, self.watervibe_user.ounces_in_a_day)
		self.assertEqual(8.0, self.watervibe_user.drink_size)