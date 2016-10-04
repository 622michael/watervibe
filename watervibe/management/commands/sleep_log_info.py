from django.core.management.base import BaseCommand, CommandError
from watervibe import users
from watervibe import stats
from watervibe.watervibe_time import string_for_day, date_for_string, now_in_user_timezone
from watervibe.models import Event, User
import importlib
from datetime import timedelta

class Command(BaseCommand):
        def handle(self, *args, **options):
        	for user in User.objects.all():
	        	for day in range(0, 8):
	        		for event in Event.objects.filter(day_of_week = day, user = user):
	        			print "%s:" % string_for_day(day)
	        			print "\t -- SLEEP: %f - %f" % (event.start_time, event.end_time)
	        			print "\t \t Probability: %f" % event.probability
	        			print "\t \t Variance: %f" % event.probability_variance
	        			print "\t \t Fringe Probability: %f" % event.fringe_probability
	        			print "\t \t Fringe Variance: %f" % event.fringe_variance
						
