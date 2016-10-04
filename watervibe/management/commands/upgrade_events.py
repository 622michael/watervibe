from django.core.management.base import BaseCommand, CommandError
from watervibe.models import Event
from watervibe.watervibe_time import event_time_from_date


class Command(BaseCommand):
	def handle(self, *args, **options): 
		for event in Event.objects.all():
			
