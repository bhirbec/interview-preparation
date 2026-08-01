def total_fruit(fruits):
  counts = {}
  best = 0
  left = 0

  for right, fruit in enumerate(fruits):
    counts[fruit] = counts.get(fruit, 0) + 1

    # More than two baskets in use: drop trees from the left until one of the
    # types disappears from the window.
    while len(counts) > 2:
      leaving = fruits[left]
      counts[leaving] -= 1
      if counts[leaving] == 0:
        del counts[leaving]
      left += 1

    best = max(best, right - left + 1)

  return best
