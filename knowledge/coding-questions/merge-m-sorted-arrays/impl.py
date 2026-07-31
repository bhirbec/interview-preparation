# Merge M Sorted Arrays
#
# Difficulty: medium
# Source: https://www.glassdoor.com/Interview/You-are-given-a-collection-of-M-arrays-with-N-integers-Every-array-is-sorted-Develop-an-algorithm-to-combine-each-array-i-QTN_1195702.htm
# Tags: #array #heap #sorting #google
#
# You are given a collection of arrays, each of which is already sorted in
# non-decreasing order. Merge them into a single array sorted in non-decreasing
# order and return it.
#
# Constraints:
#   - There may be any number of input arrays, including zero.
#   - Individual arrays may be empty and may have different lengths.
#   - Values are integers and may be negative or duplicated.
#
# Examples:
#   [[1, 4, 7], [2, 5], [3, 6]]        -> [1, 2, 3, 4, 5, 6, 7]
#   [[1, 1, 45], [1, 4, 23]]           -> [1, 1, 1, 4, 23, 45]
#   [[], [2], []]                      -> [2]
#   []                                 -> []
#
# Approach: push the head of each non-empty array into a min-heap, then
# repeatedly pop the smallest and push the next element from the same array
# (O(total * log m)).


def merge_sorted_arrays(arrays):
  # TODO: implement
  raise NotImplementedError
