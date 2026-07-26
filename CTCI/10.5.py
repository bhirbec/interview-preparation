# Sparse Search
# Difficulty: easy
# Tags: #binary-search #array #string
#
# You are given a sorted array of strings interspersed with empty strings
# (`''`), and a target non-empty string `value`. Return an index at which
# `value` occurs, or None if it is not present.
#
# Input:  a sorted list of strings (some of which may be ''), and a target.
# Output: an index i with arr[i] == value, or None if absent.
#
# The empty strings break a plain binary search because you cannot compare
# against them. Approach: probe within [start, end]; if the probe lands on an
# empty string, retry after trimming empty ends; otherwise recurse into the
# left or right half by comparing against the probe. (This implementation
# picks the probe index at random, which stays correct because empty ends are
# trimmed each step, guaranteeing progress.)
#
# Examples:
#   arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']
#   binary_search(arr, 'ball') -> 4
#   binary_search(arr, 'xxx')  -> None
#   binary_search([], 'xxx')   -> None

import unittest
from random import randint


def binary_search(arr, value):
  def _f(arr, start, end):
    if end < start:
      return None

    p = randint(start, end)
    if value == arr[p] and arr[p] != '':
      return p

    if arr[start] == '':
      start += 1
    if arr[end] == '':
      end -= 1

    if arr[p] == '':
      return _f(arr, start, end)
    elif value < arr[p]:
      return _f(arr, start, p - 1)
    else:
      return _f(arr, p + 1, end)

  return _f(arr, 0, len(arr) - 1)


class TestSearch(unittest.TestCase):
  def setUp(self):
    self.arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']

  def test_search_middle(self):
    self.assertEqual(binary_search(self.arr, 'ball'), 4)

  def test_search_start(self):
    self.assertEqual(binary_search(self.arr, 'at'), 0)

  def test_search_end(self):
    self.assertEqual(binary_search(self.arr, 'dad'), 10)

  def test_not_found(self):
    self.assertIsNone(binary_search(self.arr, 'xxx'))

  def test_empty_array(self):
    self.assertIsNone(binary_search([], 'xxx'))

  def test_all_empty_strings(self):
    self.assertIsNone(binary_search(['', '', '', '', '', '', ''], 'xxx'))

  def test_single_target_among_empties(self):
    self.assertEqual(binary_search(['', '', '', 'a', '', '', ''], 'a'), 3)

  def test_correctness_over_many_runs(self):
    # The probe is random, so exercise it repeatedly: present values must be
    # located, absent values must return None, every time.
    present = {'at', 'ball', 'car', 'dad'}
    for _ in range(500):
      for v in ['at', 'ball', 'car', 'dad', 'xxx', 'aaa', 'zzz']:
        r = binary_search(self.arr, v)
        if v in present:
          assert r is not None
          self.assertEqual(self.arr[r], v)
        else:
          self.assertIsNone(r)


if __name__ == '__main__':
  unittest.main()
