def find_peak_element(nums):
  low = 0
  high = len(nums) - 1

  # Invariant: the range [low, high] always contains a peak. An ascending step
  # at mid means the climb continues to the right, so a peak lies after mid;
  # otherwise mid is itself the top of a descent and can be kept.
  while low < high:
    mid = (low + high) // 2
    if nums[mid] < nums[mid + 1]:
      low = mid + 1
    else:
      high = mid

  return low
