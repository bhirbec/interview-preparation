def edit_distance(a, b):
  m, n = len(a), len(b)
  dp = [[0] * (n + 1) for _ in range(m + 1)]
  for i in range(m + 1):
    dp[i][0] = i
  for j in range(n + 1):
    dp[0][j] = j
  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if a[i - 1] == b[j - 1]:
        dp[i][j] = dp[i - 1][j - 1]
      else:
        dp[i][j] = 1 + min(dp[i][j - 1],      # insert
                           dp[i - 1][j],      # delete
                           dp[i - 1][j - 1])  # replace
  return dp[m][n]
