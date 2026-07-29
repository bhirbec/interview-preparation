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


def merge(arr1, arr2):
  # TODO: implement
  raise NotImplementedError
