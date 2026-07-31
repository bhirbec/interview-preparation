def product_except_self(nums):
  n = len(nums)
  out = [1] * n

  prefix = 1
  for i in range(n):
    out[i] = prefix
    prefix *= nums[i]

  suffix = 1
  for i in range(n - 1, -1, -1):
    out[i] *= suffix
    suffix *= nums[i]

  return out
