import random


def kth_smallest(nums, k):
  # Quickselect: average O(n), no full sort.
  target = k - 1
  lo, hi = 0, len(nums) - 1
  nums = list(nums)  # do not mutate the caller's list
  while True:
    if lo == hi:
      return nums[lo]
    pivot = nums[random.randint(lo, hi)]
    left, mid, right = [], [], []
    for x in nums[lo:hi + 1]:
      if x < pivot:
        left.append(x)
      elif x == pivot:
        mid.append(x)
      else:
        right.append(x)
    if target < lo + len(left):
      nums[lo:hi + 1] = left + mid + right
      hi = lo + len(left) - 1
    elif target < lo + len(left) + len(mid):
      return pivot
    else:
      nums[lo:hi + 1] = left + mid + right
      lo = lo + len(left) + len(mid)
