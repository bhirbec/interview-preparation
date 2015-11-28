# There are two sorted arrays A and B of size m and n respectively.
# Find the median of the two sorted arrays. The overall run time
# complexity should be O(log (m+n)).

def median_sort(A, B):
	C = A+B
	C.sort()
	return C[len(C)/2]

def median_merge(A, B):
	n = len(A)
	i, j = 0, 0

	while i + j <= n:
		if j == n or (i < n and A[i] < B[j]):
			med = A[i]
			i += 1
		else:
			med = B[j]
			j += 1

	return med

def test(A, B):
	med1 = median_sort(A, B)
	med2 = median_merge(A, B)
	print med1 == med2


def main():
	A = [1, 2, 3, 5]
	B = [2, 7, 9, 10]
	test(A, B)

	B = [1, 1, 1, 1]
	A = [2, 7, 9, 10]
	test(A, B)

	A = [1, 1, 1, 1]
	B = [2, 7, 9, 10]
	test(A, B)


main()
