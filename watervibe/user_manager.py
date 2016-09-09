from datetime import datetime
import dateutil.parser


def period_for_user (user):
	default_start_value = '08:30-04:00'
	default_end_value = '20:30-04:00'

	return dateutil.parser.parse(default_start_value), dateutil.parser.parse(default_end_value)