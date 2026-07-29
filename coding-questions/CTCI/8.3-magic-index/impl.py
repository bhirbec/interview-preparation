# Magic Index
# Difficulty: medium
# Tags: #array #binary-search #recursion
#
# A magic index in an array A is an index i such that A[i] == i. Given a sorted
# array of DISTINCT integers, return a magic index if one exists, or -1 if there
# is none.
#
# Input: array, a list of distinct ints sorted in ascending order.
# Output: an index i with array[i] == i, or -1 if no such index exists.
#
# Examples:
#   [-4, -2, 2, 3, 10] -> 2  (array[2] == 2)
#   [-1, 1, 3, 5, 7]   -> 1  (array[1] == 1)
#   [-1, 0, 3, 5, 7]   -> -1 (no index equals its value)
#   [1, 2, 3, 4, 5]   -> -1  (no magic index)
#   []                -> -1
#
# Approach: because the values are distinct and sorted, a binary search works.
# If array[mid] > mid the magic index (if any) must be on the left; if
# array[mid] < mid it must be on the right.

import unittest


def magic_index_distinct_array(array):
  '''
  Time: O(log(n))
  space: O(log(n))
  '''
  n = len(array)

  def _f(i, j):
    if j < i:
      return -1

    index = int((i + j) / 2)
    if array[index] == index:
      return index
    elif array[index] > index:
      return _f(i, index - 1)
    else:
      return _f(index + 1, j)

  return _f(0, n - 1)


class TestMagicIndex(unittest.TestCase):
  def test_magic_in_middle(self):
    self.assertEqual(magic_index_distinct_array([-4, -2, 2, 3, 10]), 2)

  def test_no_magic_realistic(self):
    self.assertEqual(magic_index_distinct_array([-1, 0, 3, 5, 7]), -1)

  def test_magic_early(self):
    self.assertEqual(magic_index_distinct_array([-1, 1, 3, 5, 7]), 1)

  def test_no_magic_all_greater(self):
    self.assertEqual(magic_index_distinct_array([1, 2, 3, 4, 5]), -1)

  def test_no_magic_all_smaller(self):
    self.assertEqual(magic_index_distinct_array([-5, -4, -3, -2, -1]), -1)

  def test_magic_at_zero(self):
    self.assertEqual(magic_index_distinct_array([0, 2, 4, 6]), 0)

  def test_magic_at_last_index(self):
    self.assertEqual(magic_index_distinct_array([-2, -1, 0, 3]), 3)

  def test_empty_array(self):
    self.assertEqual(magic_index_distinct_array([]), -1)

  def test_single_element_magic(self):
    self.assertEqual(magic_index_distinct_array([0]), 0)

  def test_single_element_no_magic(self):
    self.assertEqual(magic_index_distinct_array([5]), -1)


if __name__ == '__main__':
  unittest.main()
