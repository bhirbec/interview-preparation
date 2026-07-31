# Recursive Multiply
# Difficulty: medium
# Tags: #recursion #bit-manipulation #math
#
# Write a recursive function to multiply two non-negative integers `a` and `b`
# without using the `*` operator (or the `/` operator). You may use addition,
# subtraction, and bit shifting.
#
# Input:  two integers a >= 0 and b >= 0.
# Output: the product a * b, computed only with +, -, and bit shifts.
#
# Approach: use the identity a * b = (a * (b >> 1)) << 1, adding one extra `a`
# when the low bit of b is set. This halves b at every step, giving O(log b)
# recursive calls.
#
# Examples:
#   multiply(0, 5)   -> 0
#   multiply(7, 1)   -> 7
#   multiply(3, 4)   -> 12
#   multiply(9, 9)   -> 81


def multiply(a, b):
  # TODO: implement
  raise NotImplementedError
