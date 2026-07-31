def justify(words, width):
  n = len(words)
  # memo[i] = (min cost of laying out words[i:], index where line 1 ends)
  memo = {n: (0, None)}

  def dp(i):
    if i in memo:
      return memo[i]
    best = None
    best_j = None
    line_len = -1  # accounts for the space added before each word
    for j in range(i + 1, n + 1):
      line_len += len(words[j - 1]) + 1
      if line_len > width:
        break
      cost = (width - line_len) ** 3 + dp(j)[0]
      if best is None or cost < best:
        best, best_j = cost, j
    memo[i] = (best, best_j)
    return memo[i]

  dp(0)
  lines = []
  i = 0
  while i < n:
    j = memo[i][1]
    lines.append(" ".join(words[i:j]))
    i = j
  return lines
