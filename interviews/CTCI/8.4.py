
def subsets(S):
	n = len(S)
	buf = [''] * n
	def _f(i, d):
		if d > n:
			return

		print ''.join(buf[:d])

		for j in xrange(i, n):
			buf[d] = S[j]
			_f(j + 1, d + 1)

	_f(0, 0)

subsets('abc')
