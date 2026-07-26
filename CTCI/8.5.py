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
#
# Note: the original solution recursed forever on b == 0 (its only base case was
# b == 1). A minimal `b == 0` guard was added so the function is total on b >= 0.

import unittest


def multiply(a, b):
  if b == 0:
    return 0
  if b == 1:
    return a

  s = multiply(a, b >> 1) << 1
  if b & 1:
    s += a

  return s


class TestRecursiveMultiply(unittest.TestCase):
  def test_multiply_by_zero(self):
    self.assertEqual(multiply(0, 5), 0)
    self.assertEqual(multiply(5, 0), 0)
    self.assertEqual(multiply(0, 0), 0)

  def test_multiply_by_one(self):
    self.assertEqual(multiply(7, 1), 7)
    self.assertEqual(multiply(1, 7), 7)

  def test_small_products(self):
    self.assertEqual(multiply(3, 4), 12)
    self.assertEqual(multiply(9, 9), 81)
    self.assertEqual(multiply(6, 7), 42)

  def test_matches_builtin_over_range(self):
    for a in range(0, 40):
      for b in range(0, 40):
        self.assertEqual(multiply(a, b), a * b)

  def test_large_values(self):
    self.assertEqual(multiply(123, 123312), 123 * 123312)


if __name__ == '__main__':
  unittest.main()
