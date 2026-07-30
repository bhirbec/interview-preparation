def longest_subarray_at_most_k(a, k):
  start = 0
  total = 0
  best = 0
  for end in range(len(a)):
    total += a[end]
    while total > k:
      total -= a[start]
      start += 1
    best = max(best, end - start + 1)
  return best
