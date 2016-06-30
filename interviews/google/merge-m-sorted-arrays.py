# Google interview found on Glassdoor
# https://www.glassdoor.com/Interview/You-are-given-a-collection-of-M-arrays-with-N-integers-Every-array-is-sorted-Develop-an-algorithm-to-combine-each-array-i-QTN_1195702.htm

# You are given a collection of M sorted arrays with N integers.
# Develop an algorithm to combine each array into one sorted array.

import heapq


def main():
	a1 = [1, 1,  1,  1,  1, 45]
	a2 = [1, 4,  7,  9, 12, 23]
	a3 = [5, 6, 11, 14, 17, 22]
	a4 = [3, 4,  9, 15, 18, 32]
	print merge_naive([a1, a2, a3, a4], 6)
	print merge_with_heap([a1, a2, a3, a4], 6)


def merge_with_heap(arrays, n):
	'''
	Time: O(n * m * log(m))
	Extra space: log(m)
	'''
	m = len(arrays)
	size = n*m
	h = []
	merged = [0]*size

	for i in xrange(m):
		val = arrays[i][0]
		heapq.heappush(h, (val, i, 0))

	for k in xrange(size):
		val, i, j = heapq.heappop(h)
		merged[k] = val

		# array i isn't done
		if j < n-1:
			j += 1
			val = arrays[i][j]
			heapq.heappush(h, (val, i, j))

	return merged

def merge_naive(arrays, n):
	'''
	Time: O(n * m^2)
	'''
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
