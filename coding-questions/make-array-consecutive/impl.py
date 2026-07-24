# Make Array Consecutive
#
# Difficulty: easy
# Tags: #array #math
#
# You are given an array of distinct non-negative integers `statues`, where each
# value is the size of a statue you own. You want your collection to contain
# every size in a consecutive range with no gaps — that is, for the smallest and
# largest sizes you end up with, you must own a statue of every integer size in
# between.
#
# Return the minimum number of additional statues you need to acquire so that the
# sizes you own form such a gap-free consecutive range.
#
# Constraints:
#   - 1 <= len(statues) <= 1000
#   - 0 <= statues[i] <= 20000
#   - all values in statues are distinct
#
# Examples:
#   [6, 2, 3, 8]  -> 3   (needs 4, 5, 7 to fill 2..8)
#   [0, 3]        -> 2   (needs 1, 2)
#   [5, 4, 6]     -> 0   (already consecutive)
#   [6]           -> 0   (a single statue is trivially consecutive)
#
# Approach: answer = (max - min + 1) - len(statues), using exact integer math.

import unittest


def make_array_consecutive(statues):
  return (max(statues) - min(statues)) - len(statues) + 1


class TestMakeArrayConsecutive(unittest.TestCase):
  def test_example(self):
    self.assertEqual(make_array_consecutive([6, 2, 3, 8]), 3)

  def test_two_element_gap(self):
    self.assertEqual(make_array_consecutive([0, 3]), 2)

  def test_already_consecutive(self):
    self.assertEqual(make_array_consecutive([5, 4, 6]), 0)

  def test_single_statue(self):
    self.assertEqual(make_array_consecutive([6]), 0)

  def test_unsorted_input(self):
    self.assertEqual(make_array_consecutive([8, 3, 6, 2]), 3)

  def test_large_gap(self):
    self.assertEqual(make_array_consecutive([1, 10]), 8)

  def test_starts_at_zero(self):
    self.assertEqual(make_array_consecutive([0]), 0)

  def test_outlier_high_value(self):
    self.assertEqual(make_array_consecutive([6, 2, 3, 8, 15]), 9)


if __name__ == '__main__':
  unittest.main()
