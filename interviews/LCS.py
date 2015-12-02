# Given two string X and Y, find the longuest common subsequence.
# Example:
# X = 'HELLO'
# Y = 'MELODY'
# The expected output is 'ELO'

def main():
	s1 = 'HELLO'
	s2 = 'MELODY'
	print lcs(s1, s2, len(s1)-1, len(s2)-1)

	s1 = 'ATGCACTGAACCTGCACGT'
	s2 = 'ACTGCGCAAACGCGTTGTACGGGG'
	print lcs(s1, s2, len(s1)-1, len(s2)-1)

def lcs(s1, s2, i, j):
	memo = {}
	count = {}

	def _lcs(s1, s2, i, j):
		if i < 0 or j < 0:
			return ''

		hit = memo.get((i, j))
		if hit is not None:
			return hit

		if s1[i] == s2[j]:
			# do we need to cache this?
			return _lcs(s1, s2, i-1, j-1) + s1[i]

		seq1 = _lcs(s1, s2, i-1, j)
		memo[(i-1, j)] = seq1
		seq2 = _lcs(s1, s2, i, j-1)
		memo[(i, j-1)] = seq2
		return seq1 if len(seq1) > len(seq2) else seq2

	return _lcs(s1, s2, i, j)

main()
