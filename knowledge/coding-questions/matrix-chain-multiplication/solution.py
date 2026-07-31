from functools import lru_cache


def min_multiplications(dims):
  n = len(dims) - 1  # number of matrices
  if n < 2:
    return 0

  @lru_cache(maxsize=None)
  def dp(i, j):
    if i == j:
      return 0
    return min(
        dp(i, k) + dp(k + 1, j) + dims[i] * dims[k + 1] * dims[j + 1]
        for k in range(i, j))

  return dp(0, n - 1)
