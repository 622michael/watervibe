from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import tasks

class Command(BaseCommand):
	def add_arguments(self, parser): 
		parser.add_argument('user_id', type=int)

	def handle(self, *args, **options): 
		user = User.objects.get(id = options["user_id"])
		tasks.sync(user)

