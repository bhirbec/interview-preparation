# Sorted Search, No Size
# Difficulty: medium
# Tags: #binary-search #array
#
# You are given a `Listy`: a sorted (ascending) list-like structure of
# positive integers that does NOT expose its length. The only way to read it
# is `element_at(i)`, which returns the value at index `i`, or -1 when `i` is
# out of bounds. Given a `Listy` and a target `value`, return an index at
# which `value` appears, or None if it is not present.
#
# Input:  a Listy of sorted positive ints, and a target value.
# Output: an index i with element_at(i) == value, or None if absent.
#
# Approach: first find a right bound by doubling an index until element_at
# either overshoots the end (returns -1) or exceeds the target, then run a
# binary search within the located range.
#
# Examples:
#   Listy([1, 4, 6, 17, 21, 34]).find(6)  -> 2
#   Listy([1, 4, 6, 17, 21, 34]).find(34) -> 5
#   Listy([1, 4, 6, 17, 21, 34]).find(37) -> None
#   Listy([]).find(6)                      -> None


class Listy(object):
  def __init__(self, arr):
    self.arr = arr

  def element_at(self, i):
    try:
      return self.arr[i]
    except IndexError:
      return -1

  def find(self, value):
    # TODO: implement
    raise NotImplementedError
