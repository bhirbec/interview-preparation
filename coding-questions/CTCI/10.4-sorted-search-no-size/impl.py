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

import unittest


class Listy(object):
  def __init__(self, arr):
    self.arr = arr

  def element_at(self, i):
    try:
      return self.arr[i]
    except IndexError:
      return -1

  def find(self, value):
    def _f(first, last):
      first_val = self.element_at(first)
      last_val = self.element_at(last)

      if first_val == value:
        return first
      elif last_val == value:
        return last
      elif first >= last:
        return None
      elif last_val == -1:
        # overshot the end, so shrink the range by half
        mid = int((last + first) / 2)
        return _f(first, mid)
      elif value > last_val:
        # target is beyond the current range, so double the window
        return _f(last + 1, last * 2)
      else:
        mid = int((last + first) / 2)
        return _f(first, mid)

    return _f(0, 2)


class TestListy(unittest.TestCase):
  def test_element_at(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.element_at(0), 1)
    self.assertEqual(l.element_at(3), 17)
    self.assertEqual(l.element_at(5), 34)
    self.assertEqual(l.element_at(6), -1)
    self.assertEqual(l.element_at(11236), -1)

  def test_find_at_start(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(1), 0)

  def test_find_in_middle(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(6), 2)
    self.assertEqual(l.find(17), 3)

  def test_find_at_end(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertEqual(l.find(34), 5)

  def test_find_absent_below_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(0))

  def test_find_absent_within_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(2))
    self.assertIsNone(l.find(35))

  def test_find_absent_above_range(self):
    l = Listy([1, 4, 6, 17, 21, 34])
    self.assertIsNone(l.find(37))

  def test_find_empty(self):
    l = Listy([])
    self.assertIsNone(l.find(6))

  def test_find_single_element(self):
    self.assertEqual(Listy([5]).find(5), 0)
    self.assertIsNone(Listy([5]).find(9))
    self.assertIsNone(Listy([5]).find(1))

  def test_find_with_duplicate(self):
    l = Listy([1, 4, 6, 6, 6, 8, 9])
    self.assertIn(l.find(6), (2, 3, 4))


if __name__ == '__main__':
  unittest.main()
