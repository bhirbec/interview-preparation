# Sorted Search, No Size
#
# You are given a `Listy`: a sorted (ascending) list-like structure of
# positive integers that does NOT expose its length. The only way to read it
# is `element_at(i)`, which returns the value at index `i`, or -1 when `i` is
# out of bounds. Given a `Listy` and a target `value`, return an index at
# which `value` appears, or None if it is not present.
#
# Input:  a Listy of sorted positive ints, and a target value.
# Output: an index i with element_at(i) == value, or None if absent.


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
