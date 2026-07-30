def trap_water(heights):
  lo, hi = 0, len(heights) - 1
  left_max = right_max = 0
  total = 0
  while lo < hi:
    if heights[lo] <= heights[hi]:
      left_max = max(left_max, heights[lo])
      total += left_max - heights[lo]
      lo += 1
    else:
      right_max = max(right_max, heights[hi])
      total += right_max - heights[hi]
      hi -= 1
  return total
