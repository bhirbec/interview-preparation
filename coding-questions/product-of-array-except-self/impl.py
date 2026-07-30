# Product Of Array Except Self
#
# Difficulty: medium
# Source: https://www.glassdoor.com/Interview/google-software-engineer-interview-questions-SRCH_KE0,24.htm
# Tags: #array #google
#
# You are given an array of integers `nums`. Return an array `out` of the same
# length where out[i] is the product of every element of `nums` except nums[i].
# You must NOT use the division operator.
#
# Constraints:
#   - The array may contain zeros, negative numbers, and duplicates.
#   - The empty product (for a single-element array) is 1.
#   - Solve in O(n) time using O(1) extra space besides the output.
#
# Examples:
#   [1, 2, 3, 4]        -> [24, 12, 8, 6]
#   [-2, 12, 3, -6, 21] -> [-4536, 756, 3024, -1512, 432]
#   [0, 4, 3]           -> [12, 0, 0]     # one zero: only its slot is non-zero
#   [0, 0, 5]           -> [0, 0, 0]      # two zeros: every product is zero
#   [7]                 -> [1]            # empty product
#
# Approach: fill the output with running prefix products left-to-right, then
# multiply in the running suffix products right-to-left.


def product_except_self(nums):
  # TODO: implement
  raise NotImplementedError
