# Given two string X and Y, find the longuest common subsequence.
# Example:
# X = 'HELLO'
# Y = 'MELODY'
# The expected output is 'ELO'

def main():
    s1 = 'HELLO'
    s2 = 'MELODY'
    print lcs_recursive(s1, s2)
    print lcs_bottom_up(s1, s2)

    s1 = 'ATGCACTGAACCTGCACGT'
    s2 = 'ACTGCGCAAACGCGTTGTACGGGG'
    print lcs_recursive(s1, s2)
    print lcs_bottom_up(s1, s2)

def lcs_recursive(s1, s2):
    n1, n2 = len(s1), len(s2)
    memo = [[-1 for _ in xrange(n2+1)] for _ in xrange(n1+1)]

    def _lcs(i, j):
        if i < 0 or j < 0:
            return 0

        hit = memo[i][j]
        if hit > -1:
            return hit

        if s1[i-1] == s2[j-1]:
            v = _lcs(i-1, j-1) + 1
        else:
            v = max(_lcs(i, j-1), _lcs(i-1, j))

        memo[i][j] = v
        return v

    _lcs(n1, n2)
    return reconstruct(memo, s1, s2)

def lcs_bottom_up(s1, s2):
    n1, n2 = len(s1), len(s2)
    memo = [[0 for _ in xrange(n2+1)] for _ in xrange(n1+1)]

    for i, c1 in enumerate(s1, 1):
        for j, c2 in enumerate(s2, 1):
            if c1 == c2:
                memo[i][j] = memo[i-1][j-1] + 1
            else:
                memo[i][j] = max(memo[i][j-1], memo[i-1][j])

    return reconstruct(memo, s1, s2)

def reconstruct(memo, s1, s2):
    i = len(s1)
    j = len(s2)
    path = []

    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            path.append(s1[i-1])
            i -= 1
            j -= 1
        elif memo[i-1][j] >= memo[i][j-1]:
            i -= 1
        else:
            j -= 1

    return ''.join((reversed(path)))

main()
