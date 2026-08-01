import unittest


class TestEraseOverlapIntervals(unittest.TestCase):
  def test_example(self):
    self.assertEqual(
        erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]), 1)

  def test_identical_intervals(self):
    self.assertEqual(erase_overlap_intervals([[1, 2], [1, 2], [1, 2]]), 2)

  def test_touching_endpoints_are_not_overlaps(self):
    self.assertEqual(erase_overlap_intervals([[1, 2], [2, 3]]), 0)

  def test_empty(self):
    self.assertEqual(erase_overlap_intervals([]), 0)

  def test_single_interval(self):
    self.assertEqual(erase_overlap_intervals([[5, 9]]), 0)

  def test_already_disjoint(self):
    self.assertEqual(
        erase_overlap_intervals([[1, 2], [3, 4], [5, 6]]), 0)

  def test_unsorted_input(self):
    self.assertEqual(
        erase_overlap_intervals([[5, 6], [1, 4], [2, 3], [3, 5]]), 1)

  def test_one_long_interval_swallows_many(self):
    # Dropping the single [0, 10] beats dropping the four short ones.
    intervals = [[0, 10], [1, 2], [3, 4], [5, 6], [7, 8]]
    self.assertEqual(erase_overlap_intervals(intervals), 1)

  def test_full_chain_of_overlaps(self):
    self.assertEqual(
        erase_overlap_intervals([[1, 5], [2, 6], [3, 7], [4, 8]]), 3)

  def test_negative_coordinates(self):
    self.assertEqual(
        erase_overlap_intervals([[-5, -1], [-2, 3], [-1, 0]]), 1)


if __name__ == '__main__':
  unittest.main()
