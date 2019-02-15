# Given two string X and Y, find the longuest common subsequence.
# Example:
# X = 'HELLO'
# Y = 'MELODY'
# The expected output is 'ELO'

def main():
    s1 = 'HELLO'
    s2 = 'MELODY'
    print(lcs_recursive(s1, s2))
    print(lcs_bottom_up(s1, s2))

    s1 = 'ATGCACTGAACCTGCACGT'
    s2 = 'ACTGCGCAAACGCGTTGTACGGGG'
    print(lcs_recursive(s1, s2))
    print(lcs_bottom_up(s1, s2))

    print(longuest_common_subseq1(s1, s2))
    print(longuest_common_subseq2(s1, s2))


def lcs_recursive(s1, s2):
    n1, n2 = len(s1), len(s2)
    memo = [[-1 for _ in range(n2+1)] for _ in range(n1+1)]

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
    memo = [[0 for _ in range(n2+1)] for _ in range(n1+1)]

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


def longuest_common_subseq1(s1, s2):
  n, m = len(s1), len(s2)
  mem = {}
  def _lcs(i, j):
    if i < 0 or j < 0:
      return 0

    if s1[i] == s2[j]:
      res = 1 + _lcs(i-1, j-1)
    else:
      res = max(_lcs(i-1, j), _lcs(i, j-1))

    mem[(i, j)] = res
    return res

  return _lcs(n-1, m-1)


def longuest_common_subseq2(s1, s2):
  n, m = len(s1), len(s2)
  mem = [[0 for j in range(m+1)] for i in range(n+1)]

  for i in range(1, n+1):
    for j in range(1, m+1):
      if s1[i-1] == s2[j-1]:
        res = 1 + mem[i-1][j-1]
      else:
        res = max(mem[i-1][j], mem[i][j-1])
      mem[i][j] = res

  return mem[n][m]


main()
