import unittest


def merge(arr1, arr2, i=3):
  j = len(arr2) - 1
  k = len(arr1) - 1

  while i > -1 and j > -1:
    if arr1[i] >= arr2[j]:
      arr1[k] = arr1[i]
      arr1[i] = None
      i -= 1
    else:
      arr1[k] = arr2[j]
      arr2[j] = None
      j -= 1

    k -= 1

  while j > -1:
    arr1[k] = arr2[j]
    arr2[j] = None
    j -= 1
    k -= 1


class TestMerge(unittest.TestCase):
  def test_merge(self):
    arr1 = [1, 4, 6, 17, None, None, None]
    arr2 = [3, 3, 10]
    arr = merge(arr1, arr2)
    self.assertTrue(arr1 == [1, 3, 3, 4, 6, 10, 17])

  def test_merge_empty(self):
    arr1 = [1, 4, 6, 17]
    arr2 = []
    arr = merge(arr1, arr2)
    self.assertTrue(arr1 == [1, 4, 6, 17])

    arr1 = []
    arr = merge(arr1, arr2)
    self.assertTrue(arr1 == [])

  def test_all_smaller(self):
    arr1 = [1, 4, 6, 17, None, None]
    arr2 = [-1, -1]
    arr = merge(arr1, arr2)
    self.assertTrue(arr1 == [-1, -1, 1, 4, 6, 17])

  def test_all_bigger(self):
    arr1 = [1, 4, 6, 17, None, None]
    arr2 = [21, 21]
    arr = merge(arr1, arr2)
    self.assertTrue(arr1 == [1, 4, 6, 17, 21, 21])


if __name__ == '__main__':
  unittest.main()
