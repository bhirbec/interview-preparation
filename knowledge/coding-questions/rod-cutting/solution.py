def rod_cutting(prices, n):
  dp = [0] * (n + 1)
  for length in range(1, n + 1):
    best = 0
    for cut in range(1, length + 1):
      best = max(best, prices[cut] + dp[length - cut])
    dp[length] = best
  return dp[n]
