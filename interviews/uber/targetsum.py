# https://careercup.com/question?id=6287187793412096

# WAP to take one element from each of the array add it to the target sum. Print all those three-element combinations.

# A = [1, 2, 3, 3]
# B = [2, 3, 3, 4]
# C = [1, 2, 2, 2]
# target = 7

# Result:
# [[1, 2, 4], [1, 3, 3], [1, 3, 3], [1, 3, 3], [1, 3, 3], [1, 4, 2], [2, 2, 3], [2, 2, 3], [2, 3, 2], [2, 3, 2], [3, 2, 2], [3, 2, 2]]

def main():
	A = [1, 2, 3, 3]
	B = [2, 3, 3, 4]
	C = [1, 2, 2, 2]
	print target_sum(A, B, C, 7)

def target_sum(A, B, C, target):
	sums = {}

	for a in A:
		for b in B:
			sums.setdefault(a+b, []).append([a, b])

	output = []
	for c in C:
		diff = target - c
		for a, b in sums.get(diff, []):
			output.append([a, b, c])

	return output

main()
