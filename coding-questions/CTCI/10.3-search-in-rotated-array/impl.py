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


def find(arr, value):
  # TODO: implement
  raise NotImplementedError
