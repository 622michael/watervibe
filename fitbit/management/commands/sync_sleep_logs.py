from django.core.management.base import BaseCommand, CommandError
from fitbit import users
from fitbit.models import User

## This command is tasked with downloading
## and saving sleep logs to fitbit.sleep
##

class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in User.objects.all():
			users.sync_sleep_logs(user)