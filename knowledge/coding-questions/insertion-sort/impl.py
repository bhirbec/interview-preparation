# Insertion Sort
#
# Sort a list the way you would sort a hand of cards: walk left to right and,
# for each element, slide it back over the already-sorted prefix until it sits
# in the right place.
#
# Sort the list IN PLACE and return the same list object.
#
# Insertion sort must be stable: stop sliding as soon as the element to the
# left is not strictly greater, so equal elements keep their input order.
#
# Do not build a second list, and do not call `sorted`, `list.sort`, `insert`
# or `pop` -- move elements by assignment within the list.
#
# Complexity: O(n^2) time in the average and worst case, but O(n) on an
# already-sorted list and O(1) extra space, which is why it is the usual
# fallback for very small or nearly-sorted ranges.
#
# Constraints:
#   - 0 <= len(items) <= 10^4
#   - elements are mutually comparable with <
#
# Examples:
#   [5, 2, 9, 1, 5, 6]  -> [1, 2, 5, 5, 6, 9]
#   []                  -> []
#   [1]                 -> [1]
#   [3, 2, 1]           -> [1, 2, 3]
#   ["pear", "fig"]     -> ["fig", "pear"]


def insertion_sort(items):
  # TODO: implement
  raise NotImplementedError
