from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User, Event
from watervibe.events import events

class Command(BaseCommand):
	def handle(self, *args, **options):
		for user in User.objects.all():
			events.validate_user_sleeps(user)