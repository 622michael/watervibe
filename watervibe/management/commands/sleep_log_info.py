from django.core.management.base import BaseCommand, CommandError
from watervibe import users
from watervibe import stats
from watervibe.watervibe_time import string_for_day, date_for_string, now_in_user_timezone
from watervibe.models import Time
import importlib
from datetime import timedelta

class Command(BaseCommand):
        def handle(self, *args, **options):
                for user in users.users():
                        current_time = now_in_user_timezone(user)
                        for day_value in range(0,8):
                                day = current_time + timedelta(days = day_value)
                                sleep_start_time = None
				sleep_end_time = None
				for time in Time.objects.all():
                                        probability_sleeping = stats.probability("sleep", time, user= user, day_of_week = day.isoweekday())

                                        if probability_sleeping > 0.25:
						if sleep_start_time is None:
							sleep_start_time = time
					else:
						if sleep_start_time is not None:
							sleep_end_time = time
							print "%d %s: %d:%d-%d:%d" % (user.id, string_for_day(day.isoweekday()), sleep_start_time.hour,
											sleep_start_time.minute, sleep_end_time.hour,
											sleep_end_time.minute)
							sleep_start_time = None
							sleep_end_time = None
						
