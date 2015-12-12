# Initial Status
#  0   9   9   9   9
#  1   9   9   9   9
#  1   9   3   2   3
#  2   3   2   9   2
#  9   9   9   9   1

# Day 0
# [0]  9   9   9   9
#  1   9   9   9   9
#  1   9   3   2   3
#  2   3   2   9   2
#  9   9   9   9   1

# Day 1
# [0]  9   9   9   9
# [1]  9   9   9   9
# [1]  9   3   2   3
#  2   3   2   9   2
#  9   9   9   9   1

# Day 2
# [0]  9   9   9   9
# [1]  9   9   9   9
# [1]  9   3   2   3
# [2]  3   2   9   2
#  9   9   9   9   1

# Day 3
# [0]  9   9   9   9
# [1]  9   9   9   9
# [1]  9  [3] [2] [3]
# [2] [3] [2]  9  [2]
#  9   9   9   9  [1]

# High level approach: BFS + priority queue + track max value.
# - intialize a priority queue by pushing the value at 0,0
# - while the queue is not empty:
# 	- if we alreay visited the position then continue
#   - track the maximum value
#   - return the max if we've reach the last node
# 	- add top, right, bottom and left neighbors

from heapq import heappush, heappop


def main():
	matrix = [
		[0,   9,   9,   9,   9],
		[1,   9,   9,   9,   9],
		[1,   9,   3,   2,   3],
		[2,   3,   3,   9,   2],
		[9,   9,   9,   9,   1],
	]
	print find_first_day(matrix)


def find_first_day(matrix):
	n = len(matrix)
	if n == 0:
		return -1

	heap = []
	start = matrix[0][0]
	heappush(heap, (start, 0, 0))

	visited = {}
	max_value = start
	target = n-1, n-1

	while len(heap) > 0:
		value, i, j = heappop(heap)

		# skip visited node
		if (i, j) in visited:
			continue

		# keep track of the max
		if value > max_value:
			max_value = value

		# return max when we've reached the target
		if (i, j) == target:
			return max_value

		# add top, rigth, bottom and left neighbors
		i_top = i - 1
		if i_top > 0:
			heappush(heap, (matrix[i_top][j], i_top, j))

		j_right = j + 1
		if j_right < n:
			heappush(heap, (matrix[i][j_right], i, j_right))

		i_bottom = i + 1
		if i_bottom < n:
			heappush(heap, (matrix[i_bottom][j], i_bottom, j))

		j_left = j - 1
		if j_left > 0:
			heappush(heap, (matrix[i][j_left], i, j_left))

		# mark current position as visited
		visited[(i, j)] = True


if __name__ == '__main__':
	main()
