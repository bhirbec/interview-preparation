# Three Sum (Triplets to Zero)
#
# Difficulty: medium
# Source: https://careercup.com/question?id=5735322939817984
# Tags: #array #two-pointers #sorting #twitter
#
# You are given a list of integers `nums`. Return all unique triplets
# [a, b, c] of distinct positions in the list whose values sum to zero.
#
# Two triplets that use the same three values in a different order are the same
# triplet and must appear only once. Return each triplet with its values in
# non-decreasing order, and the overall result sorted, so the output is
# deterministic.
#
# Constraints:
#   - 0 <= len(nums) <= 3000
#   - -10^5 <= nums[i] <= 10^5
#
# Examples:
#   [2, 3, 1, -2, -1, 0, 2, -3, 0]
#     -> [[-3, 0, 3], [-3, 1, 2], [-2, -1, 3], [-2, 0, 2], [-1, 0, 1]]
#   [0, 0, 0, 0]   -> [[0, 0, 0]]
#   [1, 2, 3]      -> []
#   []             -> []
#
# Approach: sort, then for each anchor index scan the remaining suffix with two
# pointers, skipping equal neighbours to avoid emitting duplicate triplets.


def three_sum_zero(nums):
  # TODO: implement
  raise NotImplementedError
