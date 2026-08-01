# Range Sum Query - Immutable
#
# Design a structure over a fixed list of integers that answers range-sum
# queries. The list never changes after construction, so the queries should be
# O(1) each even if there are many of them.
#
#   - NumArray(nums): build the structure from the list `nums`.
#   - sum_range(left, right): return the sum of nums[left..right], with both
#     ends inclusive.
#
# Constraints:
#   - 0 <= len(nums) <= 10^4
#   - 0 <= left <= right < len(nums)
#   - up to 10^4 calls to sum_range
#
# Examples:
#   a = NumArray([-2, 0, 3, -5, 2, -1])
#   a.sum_range(0, 2)  ->  1    (-2 + 0 + 3)
#   a.sum_range(2, 5)  -> -1    (3 - 5 + 2 - 1)
#   a.sum_range(0, 5)  -> -3
#   a.sum_range(3, 3)  -> -5


class NumArray(object):
  def __init__(self, nums):
    pass

  def sum_range(self, left, right):
    # TODO: implement
    raise NotImplementedError
