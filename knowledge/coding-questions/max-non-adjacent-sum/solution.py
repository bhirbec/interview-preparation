def max_non_adjacent_sum(weights):
  take, skip = 0, 0  # best including / excluding the previous element
  for w in weights:
    take, skip = skip + w, max(take, skip)
  return max(take, skip)
