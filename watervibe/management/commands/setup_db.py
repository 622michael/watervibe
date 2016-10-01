from django.core.management.base import BaseCommand, CommandError
from watervibe.models import Time

class Command(BaseCommand):
	def handle(self, *args, **options):
		for hour in range(0, 24):
			for minute in range (0, 60):
				t = Time.objects.create(hour = hour, minute = minute)
				t.save
