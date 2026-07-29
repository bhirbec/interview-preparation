# Search in Rotated Array
# Difficulty: medium
# Tags: #array #binary-search
#
# You are given a sorted array of n distinct integers that has been rotated an
# unknown number of times (e.g. [1, 2, 3, 4, 5] rotated becomes [4, 5, 1, 2, 3]).
# Given a target value, return the index at which it appears, or None if it is
# absent. Aim for O(log n) time.
#
# Input:
#   arr   -- a rotated, ascending-sorted list of distinct integers (may be empty
#            or not rotated at all).
#   value -- the integer to search for.
# Output:
#   The index of value in arr, or None if it is not present.
#
# Examples:
#   find([15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], 5)  -> 8
#   find([15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14], 15) -> 0
#   find([1, 2, 3, 4, 5], 4) -> 3            (not rotated)
#   find([4, 5, 6, 7, 0, 1, 2], 3) -> None
#
# Approach: first locate the rotation point (the index of the minimum element)
# with a binary search. That splits the array into two individually sorted runs:
# a high run arr[0 .. r-1] and a low run arr[r .. n-1]. Decide which run can
# contain the value by comparing against the endpoints, then binary-search that
# run.
#
# NOTE: the original find() compared the value against arr[r] (the minimum) and
# searched arr[0..r], so the high run was never searched -- find(15) on the
# canonical array wrongly returned None. Fixed to test arr[0..r-1] and to make
# find_rotation_point return 0 for a non-rotated array.

import unittest

CANONICAL = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14]


def find(arr, value):
  if not arr:
    return None

  r = find_rotation_point(arr)

  # arr[0 .. r-1] is the higher, left run; arr[r .. end] is the lower, right run.
  if r > 0 and arr[0] <= value <= arr[r - 1]:
    idx = binary_search(arr, value, 0, r - 1)
    if idx is not None:
      return idx

  return binary_search(arr, value, r, len(arr) - 1)


def find_rotation_point(arr):
  # A non-rotated array's minimum is at index 0.
  if arr[0] <= arr[-1]:
    return 0

  def _f(arr, start, end):
    if end - start <= 1:
      return end

    mid = (end + start) // 2

    if arr[mid] > arr[end]:
      # rotation point is in the right half
      return _f(arr, mid, end)
    else:
      # rotation point is in the left half
      return _f(arr, start, mid)

  return _f(arr, 0, len(arr) - 1)


def binary_search(arr, value, start, end):
  if end < start:
    return None

  mid = (end + start) // 2
  if arr[mid] == value:
    return mid
  elif arr[mid] > value:
    return binary_search(arr, value, start, mid - 1)
  else:
    return binary_search(arr, value, mid + 1, end)


class TestSearchInRotatedArray(unittest.TestCase):
  def test_find_rotation_point_canonical(self):
    self.assertEqual(find_rotation_point(CANONICAL), 5)

  def test_find_rotation_point_not_rotated(self):
    self.assertEqual(find_rotation_point([1, 2, 3, 4, 5]), 0)

  def test_find_value_in_low_run(self):
    self.assertEqual(find(CANONICAL, 5), 8)

  def test_find_value_in_high_run(self):
    # This is the case the original buggy version missed.
    self.assertEqual(find(CANONICAL, 15), 0)
    self.assertEqual(find(CANONICAL, 25), 4)

  def test_find_every_element(self):
    for i, v in enumerate(CANONICAL):
      self.assertEqual(find(CANONICAL, v), i, msg=f'value {v}')

  def test_missing_value(self):
    self.assertIsNone(find(CANONICAL, 100))
    self.assertIsNone(find(CANONICAL, 2))
    self.assertIsNone(find(CANONICAL, -5))

  def test_not_rotated(self):
    arr = [1, 2, 3, 4, 5]
    for i, v in enumerate(arr):
      self.assertEqual(find(arr, v), i)
    self.assertIsNone(find(arr, 6))

  def test_reverse_boundaries(self):
    # Rotation such that the pivot sits near either end.
    self.assertEqual(find([2, 3, 4, 5, 1], 1), 4)   # pivot at last index
    self.assertEqual(find([5, 1, 2, 3, 4], 5), 0)   # pivot right after index 0
    self.assertEqual(find([5, 1, 2, 3, 4], 1), 1)

  def test_two_elements(self):
    self.assertEqual(find([1, 2], 1), 0)
    self.assertEqual(find([1, 2], 2), 1)
    self.assertEqual(find([2, 1], 1), 1)
    self.assertEqual(find([2, 1], 2), 0)

  def test_single_element(self):
    self.assertEqual(find([5], 5), 0)
    self.assertIsNone(find([5], 3))

  def test_empty(self):
    self.assertIsNone(find([], 1))


if __name__ == '__main__':
  unittest.main()
