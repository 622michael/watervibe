from django.core.management.base import BaseCommand, CommandError
from fitbit.models import User
from fitbit import subscription

## This command subscribes all users to 
## the sleep notification API. It should
## be run only in testing. (Users are
## automatically subscribed to the FitBit API.
class Command(BaseCommand):
	def handle(self, *args, **options):

		for user in User.objects.all():
			subscription.subscribitions_for_user(user)
			subscription.subscribe(user, "sleep")
