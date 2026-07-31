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


def magic_index_distinct_array(array):
  # TODO: implement
  raise NotImplementedError
