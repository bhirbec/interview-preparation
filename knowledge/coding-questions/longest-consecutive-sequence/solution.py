def longest_consecutive(nums):
  values = set(nums)
  best = 0

  for n in values:
    # Only the smallest value of a run does the walking, so every run is
    # traversed once and the total work stays linear in the number of values.
    if n - 1 in values:
      continue

    length = 1
    while n + length in values:
      length += 1

    best = max(best, length)

  return best
