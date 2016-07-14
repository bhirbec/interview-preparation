
def bottom_up(items, W):
	n = len(items)
	A = [[0 for _ in xrange(W+1)] for _ in xrange(n)]

	for i, (vi, wi) in enumerate(items):
		for x in xrange(W+1):
			if wi > x:
				A[i][x] = A[i-1][x]
			else:
				A[i][x] = max(A[i-1][x], A[i-1][x-wi] + vi)

	return _reconstruct_solution(A, items, W)

def _reconstruct_solution(A, items, W):
	S = []
	i = len(items) - 1
	x = W

	while i >= 0 and x >= 0:
		vi, wi = items[i]
		if wi > x or A[i-1][x] > A[i-1][x-wi] + vi:
			pass # we do not pick this item
		else:
			S.append(i)
			x -= wi
		i -= 1

	S.reverse()
	return S

if __name__ == '__main__':
	items = [
		(1, 7), # value, weight
		(4, 2),
		(5, 4),
		(7, 5),
	]
	W = 9
	print bottom_up(items, W)
