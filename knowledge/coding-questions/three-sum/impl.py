# Three Sum
#
# Difficulty: medium
# Source: https://www.glassdoor.com/Interview/3-sum-problem-that-can-be-found-on-leetcode-QTN_1202200.htm
# Source: https://en.wikipedia.org/wiki/3SUM
# Tags: #array #two-pointers #sorting #google
#
# You are given an array of integers `nums` and an integer `target`. Return all
# unique triplets (a, b, c) drawn from three DISTINCT positions of `nums` whose
# values sum to `target`.
#
# Two triplets are considered the same if they contain the same multiset of
# values, so the result must not contain duplicates. Return each triplet with its
# values in non-decreasing order, and the list of triplets sorted.
#
# Constraints:
#   - 0 <= len(nums)
#   - values may be negative, zero, or positive, and may repeat
#
# Examples:
#   nums = [-1, 0, 1, 2, -1, -4], target = 0
#     -> [(-1, -1, 2), (-1, 0, 1)]
#   nums = [0, 0, 0, 0], target = 0
#     -> [(0, 0, 0)]                # only one unique triplet despite duplicates
#   nums = [1, 2, 3], target = 100
#     -> []                         # no triplet reaches the target
#   nums = [-2, 0, 1, 1, 2], target = 0
#     -> [(-2, 0, 2), (-2, 1, 1)]
#
# Approach: sort the array, then for each index i sweep the remainder with two
# pointers, skipping equal neighbors to avoid duplicate triplets. O(n^2).


def three_sum(nums, target):
  # TODO: implement
  raise NotImplementedError
