# Sorted Merge
# Difficulty: easy
# Tags: #array #sorting #two-pointers
#
# You are given two sorted arrays, arr1 and arr2. arr1 already holds its own
# sorted elements at the front, followed by a trailing buffer of exactly
# len(arr2) empty (None) slots. Merge arr2 into arr1 in sorted order, in place,
# using the buffer.
#
# Input:
#   arr1 -- a list whose first (len(arr1) - len(arr2)) entries are sorted real
#           values, and whose last len(arr2) entries are None (the buffer).
#   arr2 -- a sorted list of values to merge into arr1.
# Output:
#   arr1, mutated in place to contain all values sorted ascending (also returned
#   for convenience).
#
# Constraints:
#   - arr1 must have room: len(arr1) == real_count + len(arr2).
#   - Both inputs are individually sorted ascending.
#
# Examples:
#   merge([1, 4, 6, 17, None, None, None], [3, 3, 10]) -> [1, 3, 3, 4, 6, 10, 17]
#   merge([1, 4, 6, 17], []) -> [1, 4, 6, 17]
#   merge([1, 4, 6, 17, None, None], [-1, -1]) -> [-1, -1, 1, 4, 6, 17]
#
# Approach: fill arr1 from the back. Two read pointers walk the real portion of
# arr1 and arr2 from their high ends; the larger element is written to the next
# open slot at the tail. Working backwards means the buffer is always ahead of
# the read pointer, so no unread value is overwritten.

import unittest


def merge(arr1, arr2):
  # i indexes the last real (non-buffer) element of arr1. The buffer occupies
  # the final len(arr2) slots, so the real elements end at this index. The
  # original hardcoded i = 3, which only worked for the demo input.
  i = len(arr1) - len(arr2) - 1
  j = len(arr2) - 1
  k = len(arr1) - 1

  while i > -1 and j > -1:
    if arr1[i] >= arr2[j]:
      arr1[k] = arr1[i]
      i -= 1
    else:
      arr1[k] = arr2[j]
      j -= 1
    k -= 1

  # Any remaining arr2 elements are smaller than every placed value; copy them.
  while j > -1:
    arr1[k] = arr2[j]
    j -= 1
    k -= 1

  return arr1


class TestSortedMerge(unittest.TestCase):
  def test_canonical(self):
    arr1 = [1, 4, 6, 17, None, None, None]
    self.assertEqual(merge(arr1, [3, 3, 10]), [1, 3, 3, 4, 6, 10, 17])

  def test_empty_arr2_leaves_arr1_unchanged(self):
    arr1 = [1, 4, 6, 17]
    self.assertEqual(merge(arr1, []), [1, 4, 6, 17])

  def test_both_empty(self):
    self.assertEqual(merge([], []), [])

  def test_empty_arr1_fills_from_arr2(self):
    arr1 = [None, None, None]
    self.assertEqual(merge(arr1, [1, 2, 3]), [1, 2, 3])

  def test_all_arr2_smaller(self):
    arr1 = [1, 4, 6, 17, None, None]
    self.assertEqual(merge(arr1, [-1, -1]), [-1, -1, 1, 4, 6, 17])

  def test_all_arr2_bigger(self):
    arr1 = [1, 4, 6, 17, None, None]
    self.assertEqual(merge(arr1, [21, 21]), [1, 4, 6, 17, 21, 21])

  def test_interleaved(self):
    arr1 = [2, 8, 12, None, None, None]
    self.assertEqual(merge(arr1, [1, 9, 20]), [1, 2, 8, 9, 12, 20])

  def test_duplicates_across_arrays(self):
    arr1 = [5, 5, None, None]
    self.assertEqual(merge(arr1, [5, 5]), [5, 5, 5, 5])


if __name__ == '__main__':
  unittest.main()
