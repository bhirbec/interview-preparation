# https://careercup.com/question?id=5735322939817984

# Write a function to find all the combinations of three numbers that sum to zero

# Sample input:
# [2, 3, 1, -2, -1, 0, 2, -3, 0]

# output:
# 2, -2, 0
# 1, -1, 0
# 3, -2, -1
# 3, 0, -3
# 3, 0, -3

def main():
	array = [2, 3, 1, -2, -1, 0, 2, -3, 0]
	triplets = find_triplets(array)

	for triplet in triplets.values():
		print triplet

def find_triplets(array, target_sum=0):
	h = {}
	n = len(array)

	for i in xrange(n):
		for j in xrange(i+1, n):
			s = array[i] + array[j]
			h.setdefault(s, []).append([i, j])

	triplets = {}
	for i, v in enumerate(array):
		delta = target_sum - v
		for indexes in h.get(delta, []):
			if i not in indexes:
				j, k = list(indexes)
				triplet = [array[i], array[j], array[k]]
				key = tuple(sorted(triplet))
				triplets[key] = triplet

	return triplets

main()
