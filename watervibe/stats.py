import math


def weighted_average(data_set, weight):
	total = 0.0
	count = 0.0
	for i in range(0, len(data_set)):
		x = data_set[i]
		total += x*weight(i)
		count += 1
	if count != 0:
		return total/count
	else:
		return 0
