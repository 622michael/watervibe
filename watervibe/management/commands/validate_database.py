from django.core.management.base import BaseCommand, CommandError
from watervibe.models import User, Event

class Command(BaseCommand):
	def handle(self, *args, **options):

		for user in User.objects.all():
			validate_user_sleeps(user)
			
			

	## This insures that there is an active
	## sleep event on every day of the week.
	## If there is not one is set for 8:30pm - 8:30am
	def validate_user_sleeps(user):
		for day in range(0,8):
				sleep_events = Event.objects.filter(user = user, day_of_week = day, is_active = 1, tag = "sleep")
				if len(sleep_events) == 0: 
					default_sleep_event = Event.objects.filter(user = user, day_of_week = day, tag = "sleep", start_time = 8.5, end_time = 8.5).first()

					if default_sleep_event is None: 
						default_sleep_event = Event.objects.create(user = user, day_of_week = day, tag = "sleep", start_time = 8.5, end_time = 8.5, is_active = 1)
