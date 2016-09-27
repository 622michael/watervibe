from django.core.management.base import BaseCommand, CommandError
from fitbit import users
from fitbit.models import User

class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in User.objects.all():
			users.update_profile(user)