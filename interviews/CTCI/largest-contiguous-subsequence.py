

def main():
	array = [-1, 2, 3, -3, 2, 3, 4, -4]
	print largest(array)

def largest(array):
	n = len(array)
	sum = 0
	max = 0
	i, j = 0, 0

	for k, value in enumerate(array):
		sum += value
		if sum < 0:
			sum = 0
			i = k+1
		elif sum > max:
			max = sum
			j = k

	return max, i, j

main()
