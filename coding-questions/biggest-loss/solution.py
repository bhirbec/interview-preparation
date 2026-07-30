def max_loss(prices):
  if len(prices) < 2:
    return 0

  max_so_far = prices[0]
  best = 0
  for price in prices[1:]:
    best = max(best, max_so_far - price)
    max_so_far = max(max_so_far, price)

  return best
