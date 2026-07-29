# Insertion
# Difficulty: medium
# Tags: #bit-manipulation #math
#
# You are given two 32-bit numbers, n and m, and two bit positions i and j
# (with i <= j). Insert m into n so that m occupies bits j through i of n. You
# can assume that bits j through i have enough room to fit all of m; that is, if
# m = 10011, it could be inserted at positions j = 6 and i = 2, but not at
# positions j = 5 and i = 2 (there would be no room to fit m starting at bit 2).
# Return the resulting number.
#
# Examples:
#   insert_bits(n=0b10000000000, m=0b10011, i=2, j=6) -> 0b10001001100  (1100)
#   insert_bits(n=161, m=5, i=2, j=4)                 -> 181
#   insert_bits(n=0, m=0b111, i=0, j=2)               -> 7
#   insert_bits(n=0b11111111, m=0, i=2, j=4)          -> 0b11100011 (227)
#
# Approach: build a mask that clears bits j..i of n (all ones except that
# window), apply it, then shift m left by i and OR it in.

import unittest


def insert_bits(n, m, i, j):
  left = (1 << (j + 1)) - 1
  right = (1 << i) - 1
  mask = ~(left ^ right)
  n &= mask
  m = m << i
  return n | m


class TestInsertBits(unittest.TestCase):
  def test_canonical_example(self):
    self.assertEqual(insert_bits(n=0b10000000000, m=0b10011, i=2, j=6), 0b10001001100)

  def test_second_example(self):
    self.assertEqual(insert_bits(n=161, m=5, i=2, j=4), 181)

  def test_insert_into_zero(self):
    self.assertEqual(insert_bits(n=0, m=0b111, i=0, j=2), 7)

  def test_clears_existing_bits(self):
    self.assertEqual(insert_bits(n=0b11111111, m=0, i=2, j=4), 0b11100011)

  def test_single_bit_window(self):
    self.assertEqual(insert_bits(n=0b0000, m=1, i=1, j=1), 0b0010)


if __name__ == '__main__':
  unittest.main()
