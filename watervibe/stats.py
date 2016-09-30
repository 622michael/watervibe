import math


def weighted_average(data_set, weight):
	total = 0
	count = 0
	for i in Range(0..len(data_set)-1):
		x = data_set[i]
		total += x*weight(i)
		count += 1

	return total/count