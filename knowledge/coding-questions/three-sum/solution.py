def three_sum(nums, target):
  nums = sorted(nums)
  n = len(nums)
  result = []

  for i in range(n - 2):
    if i > 0 and nums[i] == nums[i - 1]:
      continue

    lo, hi = i + 1, n - 1
    while lo < hi:
      s = nums[i] + nums[lo] + nums[hi]
      if s == target:
        result.append((nums[i], nums[lo], nums[hi]))
        lo += 1
        hi -= 1
        while lo < hi and nums[lo] == nums[lo - 1]:
          lo += 1
        while lo < hi and nums[hi] == nums[hi + 1]:
          hi -= 1
      elif s < target:
        lo += 1
      else:
        hi -= 1

  return result
