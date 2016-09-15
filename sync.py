import fitbit
import watervibes


for user in fitbit.fitbit.users():
	if not watervibes.watervibes.has_fitbit_user(user):
		watervibes.watervibes.register(user)


for user in watervibes.watervibes.users():
	for reminder in user.reminders():
		if reminder.fitbit_id is None:
			fitbit.fitbit.set_alarm (user.fitbit_user, reminder.time)