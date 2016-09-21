from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User
from watervibe import tasks

class Command(BaseCommand):
	def handle(self, *args, **options): 
		print "Success"

