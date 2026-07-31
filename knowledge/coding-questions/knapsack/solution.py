def knapsack(items, capacity):
  dp = [0] * (capacity + 1)
  for value, weight in items:
    # Descend so each item is considered at most once per capacity.
    for x in range(capacity, weight - 1, -1):
      dp[x] = max(dp[x], dp[x - weight] + value)
  return dp[capacity]
