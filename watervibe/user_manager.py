from datetime import datetime

def period_for_user (user):
	user.start_of_period = "2016-09-08 8:30"
	user.end_of_period = "2016-09-08 20:30"
	user.save()

	return datetime.strptime(user.start_of_period), datetime.strptime(user.end_of_period)