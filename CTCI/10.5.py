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
      return _f(arr, start, p-1)
    else:
      return _f(arr, p+1, end)

  return _f(arr, 0, len(arr) - 1)


class TestSearch(unittest.TestCase):
  def test_search(self):
    arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']
    self.assertTrue(binary_search(arr, 'ball') == 4)

  def test_not_found(self):
    arr = ['at', '', '', '', 'ball', '', '', 'car', '', '', 'dad', '', '']
    self.assertTrue(binary_search(arr, 'xxx') == None)

  def test_empty_array(self):
    arr = []
    self.assertTrue(binary_search(arr, 'xxx') == None)

  def test_many_empty_strings(self):
    arr = ['', '', '', '', '', '', '']
    self.assertTrue(binary_search(arr, 'xxx') == None)

    arr = ['', '', '', 'a', '', '', '']
    self.assertTrue(binary_search(arr, 'a') == 3)


if __name__ == '__main__':
  unittest.main()
