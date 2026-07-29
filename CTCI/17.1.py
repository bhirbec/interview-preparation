# Add Without Plus
# Difficulty: easy
# Tags: #bit-manipulation #math
#
# Add two integers `a` and `b` without using the `+` (or `-`) operator.
# Return their sum.
#
# Input:  two integers a and b (may be negative or zero).
# Output: the integer a + b, computed with bitwise operations only.
#
# Approach: `a ^ b` adds bit positions without carrying; `(a & b) << 1` is the
# carry. Repeat until there is no carry left. Because Python integers are
# unbounded, negatives are handled by masking to 32-bit two's complement so
# the carry terminates and the sign is reconstructed from the top bit.
#
# NOTE: the original implementation only worked for non-negative inputs — with
# a negative operand the carry propagated forever (Python ints never overflow),
# causing infinite recursion. Fixed here with 32-bit masking.
#
# Examples:
#   add(5, 3)   -> 8
#   add(0, 0)   -> 0
#   add(7, 0)   -> 7
#   add(-3, 5)  -> 2
#   add(-4, -6) -> -10

import unittest

MASK = 0xFFFFFFFF
INT_MAX = 0x7FFFFFFF


def add(a, b):
  a &= MASK
  b &= MASK
  while b != 0:
    carry = (a & b) << 1
    a = (a ^ b) & MASK
    b = carry & MASK
  # Reinterpret the 32-bit result as a signed two's-complement integer.
  return a if a <= INT_MAX else a - (MASK + 1)


class TestAdd(unittest.TestCase):
  def test_positive(self):
    self.assertEqual(add(5, 3), 8)
    self.assertEqual(add(123, 877), 1000)

  def test_zero(self):
    self.assertEqual(add(0, 0), 0)
    self.assertEqual(add(7, 0), 7)
    self.assertEqual(add(0, 42), 42)

  def test_negative_and_positive(self):
    self.assertEqual(add(-3, 5), 2)
    self.assertEqual(add(5, -3), 2)
    self.assertEqual(add(-10, 4), -6)

  def test_both_negative(self):
    self.assertEqual(add(-4, -6), -10)
    self.assertEqual(add(-1, -1), -2)

  def test_result_zero_from_opposites(self):
    self.assertEqual(add(9, -9), 0)

  def test_exhaustive_small_range(self):
    for a in range(-50, 51):
      for b in range(-50, 51):
        self.assertEqual(add(a, b), a + b)


if __name__ == '__main__':
  unittest.main()
