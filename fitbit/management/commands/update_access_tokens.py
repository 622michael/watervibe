from django.core.management.base import BaseCommand, CommandError
from fitbit import authorization
from fitbit.models import User

class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in User.objects.all():
			authorization.refresh_access_for_user(user)
