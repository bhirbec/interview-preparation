
def main():
	for p in place_queens(16):
		print p

def place_queens(n):
	queens = [0] * n
	return _place(n, 0, queens)

def _place(n, r, queens):
	if r > n-1:
		yield list(queens)
		return

	for c in xrange(n):
		if is_valid(r, c, queens):
			queens[r] = c
			for p in _place(n, r+1, queens):
				yield p

def is_valid(r, c, queens):
	for row in xrange(r):
		col_delta = abs(c - queens[row])
		if col_delta == 0:
			return False

		row_delta = r - row
		if col_delta == row_delta:
			return False

	return True

main()
