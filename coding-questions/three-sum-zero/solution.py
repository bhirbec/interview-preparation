def three_sum_zero(nums):
  nums = sorted(nums)
  n = len(nums)
  result = []
  for i in range(n - 2):
    if i > 0 and nums[i] == nums[i - 1]:
      continue
    lo, hi = i + 1, n - 1
    while lo < hi:
      total = nums[i] + nums[lo] + nums[hi]
      if total < 0:
        lo += 1
      elif total > 0:
        hi -= 1
      else:
        result.append([nums[i], nums[lo], nums[hi]])
        lo += 1
        hi -= 1
        while lo < hi and nums[lo] == nums[lo - 1]:
          lo += 1
        while lo < hi and nums[hi] == nums[hi + 1]:
          hi -= 1
  return result
