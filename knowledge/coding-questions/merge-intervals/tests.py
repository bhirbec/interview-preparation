import unittest


class TestMergeIntervals(unittest.TestCase):
  def test_example(self):
    self.assertEqual(
        merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]),
        [[1, 6], [8, 10], [15, 18]])

  def test_touching_endpoints_merge(self):
    self.assertEqual(merge_intervals([[1, 4], [4, 5]]), [[1, 5]])

  def test_fully_contained_interval(self):
    self.assertEqual(merge_intervals([[1, 4], [2, 3]]), [[1, 4]])

  def test_empty(self):
    self.assertEqual(merge_intervals([]), [])

  def test_single_interval(self):
    self.assertEqual(merge_intervals([[5, 7]]), [[5, 7]])

  def test_no_overlap_unsorted_input(self):
    self.assertEqual(
        merge_intervals([[8, 10], [1, 2], [4, 5]]),
        [[1, 2], [4, 5], [8, 10]])

  def test_all_merge_into_one(self):
    self.assertEqual(merge_intervals([[3, 6], [1, 3], [5, 9], [8, 8]]), [[1, 9]])

  def test_duplicate_intervals(self):
    self.assertEqual(merge_intervals([[2, 4], [2, 4]]), [[2, 4]])

  def test_point_intervals(self):
    self.assertEqual(merge_intervals([[1, 1], [3, 3], [1, 1]]), [[1, 1], [3, 3]])

  def test_negative_coordinates(self):
    self.assertEqual(merge_intervals([[-5, -2], [-3, 0], [1, 2]]),
                     [[-5, 0], [1, 2]])

  def test_chain_of_touching_intervals(self):
    self.assertEqual(merge_intervals([[1, 2], [2, 3], [3, 4]]), [[1, 4]])


if __name__ == '__main__':
  unittest.main()
