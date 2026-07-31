# Maximum Subarray
#
# You are given an array of integers (which may be positive or negative). Find
# the contiguous subarray with the largest sum and return that sum together
# with the start and end indices of the subarray, as a tuple
# (max_sum, start, end).
#
# If every element is negative (or the array is empty), the largest achievable
# sum is 0 — obtained by choosing the empty subarray — and (0, 0, 0) is
# returned; the indices are unused in that case.
#
# Constraints:
#   - 0 <= len(array)
#   - array values may be negative, zero, or positive
#
# Examples:
#   [-1, 2, 3, -3, 2, 3, 4, -4]     -> (11, 1, 6)   (subarray [2, 3, -3, 2, 3, 4])
#   [-2, 1, -3, 4, -1, 2, 1, -5, 4] -> (6, 3, 6)    (subarray [4, -1, 2, 1])
#   [5]                             -> (5, 0, 0)
#   [-1, -2, -3]                    -> max sum 0     (empty subarray wins)
#   []                             -> (0, 0, 0)


def max_subarray(array):
  # TODO: implement
  raise NotImplementedError
