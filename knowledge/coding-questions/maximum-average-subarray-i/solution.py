def find_max_average(nums, k):
  window = sum(nums[:k])
  best = window

  # Fixed-width window: each step adds the entering value and drops the one
  # that just fell out of range, so the sum stays O(1) per position.
  for i in range(k, len(nums)):
    window += nums[i] - nums[i - k]
    if window > best:
      best = window

  return best / float(k)
