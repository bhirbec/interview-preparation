def sorted_squares(nums):
  result = [0] * len(nums)
  left = 0
  right = len(nums) - 1

  # The biggest square sits at one end (most negative or most positive), so
  # fill the output right to left, consuming whichever end is larger.
  for slot in range(len(nums) - 1, -1, -1):
    left_square = nums[left] * nums[left]
    right_square = nums[right] * nums[right]
    if left_square > right_square:
      result[slot] = left_square
      left += 1
    else:
      result[slot] = right_square
      right -= 1

  return result
