# Google interview found on Glassdoor
# https://www.glassdoor.com/Interview/You-are-given-a-collection-of-M-arrays-with-N-integers-Every-array-is-sorted-Develop-an-algorithm-to-combine-each-array-i-QTN_1195702.htm

# You are given a collection of M sorted arrays with N integers.
# Develop an algorithm to combine each array into one sorted array.

def main():
	a1 = [1, 1,  1,  1,  1, 1]
	a2 = [2, 4,  7,  9, 12, 23]
	a3 = [5, 6, 11, 14, 17, 22]
	a4 = [3, 4,  9, 15, 18, 32]
	print merge([a1, a2, a3, a4], 6)

def merge(arrays, n):
	m = len(arrays)
	positions = [0]*m
	merged = [0]*n*m

	for k in xrange(n*m):
		min_value = 0
		selected_i = 0

		# initialize the min
		for i in xrange(m):
			pos = positions[i]
			if pos < n:
				selected_i = i
				min_value = arrays[i][pos]
				break

		# find the min
		for i in xrange(selected_i+1, m):
			pos = positions[i]
			if pos < n:
				value = arrays[i][pos]
				if value < min_value:
					min_value = value
					selected_i = i

		merged[k] = min_value
		positions[selected_i] += 1

	return merged

if __name__ == '__main__':
	main()
