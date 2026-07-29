import unittest


class TestSortedMerge(unittest.TestCase):
  def test_canonical(self):
    arr1 = [1, 4, 6, 17, None, None, None]
    self.assertEqual(merge(arr1, [3, 3, 10]), [1, 3, 3, 4, 6, 10, 17])

  def test_empty_arr2_leaves_arr1_unchanged(self):
    arr1 = [1, 4, 6, 17]
    self.assertEqual(merge(arr1, []), [1, 4, 6, 17])

  def test_both_empty(self):
    self.assertEqual(merge([], []), [])

  def test_empty_arr1_fills_from_arr2(self):
    arr1 = [None, None, None]
    self.assertEqual(merge(arr1, [1, 2, 3]), [1, 2, 3])

  def test_all_arr2_smaller(self):
    arr1 = [1, 4, 6, 17, None, None]
    self.assertEqual(merge(arr1, [-1, -1]), [-1, -1, 1, 4, 6, 17])

  def test_all_arr2_bigger(self):
    arr1 = [1, 4, 6, 17, None, None]
    self.assertEqual(merge(arr1, [21, 21]), [1, 4, 6, 17, 21, 21])

  def test_interleaved(self):
    arr1 = [2, 8, 12, None, None, None]
    self.assertEqual(merge(arr1, [1, 9, 20]), [1, 2, 8, 9, 12, 20])

  def test_duplicates_across_arrays(self):
    arr1 = [5, 5, None, None]
    self.assertEqual(merge(arr1, [5, 5]), [5, 5, 5, 5])


if __name__ == '__main__':
  unittest.main()
