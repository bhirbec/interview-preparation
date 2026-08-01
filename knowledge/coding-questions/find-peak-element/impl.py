# Find Peak Element
#
# A peak element is one that is strictly greater than both of its neighbours.
# You are given a list `nums`; return the index of any peak. Treat the values
# just outside the array as negative infinity, so nums[0] is a peak when it is
# greater than nums[1], and the last element is a peak when it is greater than
# the one before it.
#
# `nums` may contain several peaks — returning the index of any one of them is
# correct. Adjacent values are never equal, which is what makes an O(log n)
# solution possible: a binary search can always tell which half still holds a
# peak.
#
# Constraints:
#   - 1 <= len(nums) <= 10^5
#   - nums[i] != nums[i + 1] for every valid i
#   - aim for O(log n) time
#
# Examples:
#   [1, 2, 3, 1]           -> 2         (nums[2] == 3 is a peak)
#   [1, 2, 1, 3, 5, 6, 4]  -> 1 or 5    (both are peaks)
#   [1]                    -> 0
#   [3, 2, 1]              -> 0


def find_peak_element(nums):
  # TODO: implement
  raise NotImplementedError
