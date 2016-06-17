# Problem:
# For a vector of size N, find its LIS

# Example:
# D = 3, 2, 6, 4, 5 1
# LIS = 2, 4, 5

# 1.Naive Algo:
# *************

# for i=N; i>0l i-- {
# 	find all subsequence of D with length i
# 	if there is one subsequence:
# 		break
# }

# Time complexity: O(2^N)

# Dynamic Programming Algorithm
# *****************************

# subproblem: we define a vector L such that:
# - L[i] = LIS of D that end with D[i]
# - L[0] = {D[0]}

# D = 3, 2, 6, 4, 5 1
# L[0] = {3}
# L[1] = {2}
# L[2] = {2, 6}
# L[3] = {2, 4}
# L[4] = {2, 4, 5}
# L[5] = {1}

# General formula:
# L[i] = MAX(L[i] | i<j, D[j] < D[i]) + D[i]

# Time Complexity: O(n^2)

def longest_incr_subseq(seq):
	'''
	Return the LIS for a given sequence.
	https://www.youtube.com/watch?v=4fQJGoeW5VE](https://www.youtube.com/watch?v=4fQJGoeW5VE
	'''

	n = len(seq)
	subseqs = [[] for v in seq]
	subseqs[0] = [seq[0]]

	for i in xrange(1, n):
		for j in xrange(0, i):
			if seq[j] < seq[i] and len(subseqs[i]) < len(subseqs[j]):
				subseqs[i] = list(subseqs[j]) # remove copy

		subseqs[i].append(seq[i])

	longest = subseqs[0]
	for i in xrange(1, n):
		if len(subseqs[i]) > len(longest):
			longest = subseqs[i]

	return longest


def size_of_longest_incr_subseq(seq):
	'''
	Return the size of the LIS for a given sequence.
	https://www.youtube.com/watch?v=CE2b_-XfVDk
	'''

	n = len(seq)
	lis = [1 for i in seq]

	for i in xrange(1, n):
		for j in xrange(0, i):
			if seq[j] < seq[i]:
				if lis[i] < lis[j] + 1:
					lis[i] = lis[j] + 1

	return max(lis)


arr = [3, 4, -1, 0, 6, 2, 3]
print longest_incr_subseq(arr)
print size_of_longest_incr_subseq(arr)

arr = [3, 2, 6, 4, 5, 1]
print longest_incr_subseq(arr)
print size_of_longest_incr_subseq(arr)
