# Quicksort
#
# Sort a list in place with quicksort: pick a pivot, partition the range so
# that everything smaller than the pivot ends up on its left and everything
# larger on its right, then recurse into the two sides. Once partitioning has
# placed the pivot, that element is already in its final position.
#
# Sort the list IN PLACE and return the same list object.
#
# Partitioning must not allocate side lists -- swap elements within the range
# you were handed. (Building `[x for x in items if x < pivot]` and friends is
# the well-known one-liner, but it is not the algorithm being asked for and it
# costs O(n) extra space per level.)
#
# Choose the pivot as the middle element of the range rather than the first or
# last one, so an already-sorted input does not degrade to O(n^2).
#
# You may not call `sorted`, `list.sort` or any other library sort.
#
# Complexity to aim for: O(n log n) average time, O(log n) stack depth.
# Note that quicksort is not stable.
#
# Constraints:
#   - 0 <= len(items) <= 10^5
#   - elements are mutually comparable with <
#
# Examples:
#   [5, 2, 9, 1, 5, 6]  -> [1, 2, 5, 5, 6, 9]
#   []                  -> []
#   [1]                 -> [1]
#   [2, 2, 2]           -> [2, 2, 2]
#   ["pear", "fig"]     -> ["fig", "pear"]


def quicksort(items):
  # TODO: implement
  raise NotImplementedError


def partition(items, low, high):
  """Partition items[low..high] around a pivot and return the pivot's index."""
  # TODO: implement
  raise NotImplementedError
