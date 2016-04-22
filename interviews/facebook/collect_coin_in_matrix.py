# https://www.careercup.com/question?id=5722807649435648

# There are N coins with coordinates (x, y) where x > 0 and y > 0
# You start at (0, 0) and you can only do steps of form (dx, dy) where dx > 0 and dy > 0
# Print the maximum number of coins that you can collect.

# Clarification: you can do as many moves as you wish, the point is to collect maximum number
# of coins. If you are located at position (a, b) you may jump to position (a+dx, b+dy)
# for all dx > 0 and dy > 0

# We suppose we're given a m x m matrix
# Solution in O(m^3)

def main():
	coins = [(0, 1), (3, 5), (1, 8), (3, 7), (5, 0), (8, 9), (2, 4)]
	coins = sorted(coins)
	print max_coin_longest_incr_subseq(coins)

	# first attempt to solve the problem (not correct)
	coins = [(0, 1), (3, 5), (1, 8), (3, 7), (5, 0), (8, 9), (2, 4)]
	print max_coin_naive(coins)


def max_coin_longest_incr_subseq(seq):
	'''
	Compute the max number of coin we can harvest using LIS. Here's the algorithm:
	- sort coins with x coordinates
	- find size of the LIS on x, y (where both x and y increase)
	'''
	n = len(seq)
	sizes = [1 for i in xrange(n)]

	for i in xrange(1, n):
		for j in xrange(0, i):
			if seq[j][0] < seq[i][0] and seq[j][1] < seq[i][1]:
				if sizes[i] < sizes[j] + 1:
					sizes[i] = sizes[j] + 1

	return max(sizes)

def max_coin_naive(coins):
	'''
	This was my first appempt to solve the problem and did not see it was a variation of LIS.
	We have to make an assumption about the matrix size. This algorithm is not correct.
	'''

	# here's our assumption about the matrix size
	m = 10

	# 1 for coin else 0
	matrix = [ [0 for i in xrange(m)] for i in xrange(m) ]
	for x, y in coins:
		matrix[x][y] = 1

	cumuls = [[0 for i in  xrange(m)] for i in xrange(m)]
	cumuls[0][0] = matrix[0][0]

	for i in xrange(1, m):
		for j in xrange(1, m):

			max_coin = 0

			for k in xrange(0, j):
				v = cumuls[i-1][k]
				max_coin = max(v, max_coin)

			for k in xrange(0, i):
				v = cumuls[k][j-1]
				max_coin = max(v, max_coin)

			if matrix[i][j]:
				max_coin += 1

			cumuls[i][j] = max_coin

	return cumuls[m-1][m-1]

main()
