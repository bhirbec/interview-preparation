# Merge Sort
#
# Sort a list with merge sort: split it in half, sort each half recursively,
# then merge the two sorted halves back together in linear time by repeatedly
# taking the smaller of the two front elements.
#
# Return a NEW sorted list; leave the input untouched.
#
# Merge sort must be stable: when two elements compare equal, the one that came
# first in the input must still come first in the output. That falls out of the
# merge step if you take from the left half whenever the two fronts are equal.
#
# You may not call `sorted`, `list.sort` or any other library sort.
#
# Complexity to aim for: O(n log n) time in the best, average and worst case,
# and O(n) extra space.
#
# Constraints:
#   - 0 <= len(items) <= 10^5
#   - elements are mutually comparable with <
#
# Examples:
#   [5, 2, 9, 1, 5, 6]  -> [1, 2, 5, 5, 6, 9]
#   []                  -> []
#   [1]                 -> [1]
#   [3, 2, 1]           -> [1, 2, 3]
#   ["pear", "fig"]     -> ["fig", "pear"]


def merge_sort(items):
  # TODO: implement
  raise NotImplementedError


def merge(left, right):
  """Merge two already-sorted lists into one sorted list."""
  # TODO: implement
  raise NotImplementedError
