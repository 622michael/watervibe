from fitbit.tests import AppTestClass
import watervibe
from .models import User

class WaterVibeTestClass(AppTestClass):
	def test_setup(self):
		watervibe.register_fitbit_user(self.user)

		try:
			user = User.objects.filter(app_id = self.user.id)

			self.assertEqual('08:30-04:00', user.start_period)
			self.assertEqual('20:30-04:00', user.end_period)
			self.assertEqual(64.0, user.ounces_in_a_day)
			self.assertEqual(8.0, user.drink_size)
		except:
			assert("NoUser")