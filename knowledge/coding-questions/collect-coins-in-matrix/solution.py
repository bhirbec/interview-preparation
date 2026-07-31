def max_coins_collected(coins):
  coins = sorted(coins)
  n = len(coins)
  if n == 0:
    return 0

  best = [1] * n
  for i in range(1, n):
    for j in range(i):
      if coins[j][0] < coins[i][0] and coins[j][1] < coins[i][1]:
        if best[j] + 1 > best[i]:
          best[i] = best[j] + 1

  return max(best)
