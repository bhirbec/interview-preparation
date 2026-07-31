def subsets(s):
  n = len(s)
  buf = [''] * n
  result = []

  def _f(i, d):
    if d > n:
      return

    result.append(''.join(buf[:d]))

    for j in range(i, n):
      buf[d] = s[j]
      _f(j + 1, d + 1)

  _f(0, 0)
  return result
