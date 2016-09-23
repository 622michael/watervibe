from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import watervibe

class Command(BaseCommand):
	def handle(self, *args, **options): 
		users = User.objects.all()
		for user in users:
			watervibe.sync(user)

