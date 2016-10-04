from django.core.management.base import BaseCommand, CommandError
from fitbit.models import Sleep
from watervibe import watervibe 
from fitbit.fitbit_time import date_for_string

class Command(BaseCommand):
	def handle(self, *args, **options):
		for sleep in Sleep.objects.all():
			watervibe.register_sample("fitbit", sleep.user.id, "sleep", day_of_the_week = date_for_string(sleep.start_time).isoweekday())