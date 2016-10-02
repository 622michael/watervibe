from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import users, reminders
from watervibe.watervibe_time import now_in_user_timezone
import importlib
from datetime import timedelta
from watervibe import reminders

##	Add Reminders
##  --------------------------------------
##	This task is responisbile for adding 
##  reminders for all users until the
##  next sync time has all of its spots full
class Command(BaseCommand):
	def handle(self, *args, **options):
		all_users = User.objects.all().order_by('next_sync_time')

		for user in all_users:
			reminders.create_reminder_for_user(user)
