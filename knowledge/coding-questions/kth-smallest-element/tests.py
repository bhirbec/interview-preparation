import unittest


class TestKthSmallest(unittest.TestCase):
  def test_minimum(self):
    self.assertEqual(kth_smallest([7, 2, 9, 4], 1), 2)

  def test_maximum(self):
    self.assertEqual(kth_smallest([7, 2, 9, 4], 4), 9)

  def test_middle_rank(self):
    self.assertEqual(kth_smallest([7, 2, 9, 4], 2), 4)

  def test_duplicates_count_individually(self):
    self.assertEqual(kth_smallest([3, 1, 3, 2], 3), 3)

  def test_single_element(self):
    self.assertEqual(kth_smallest([5], 1), 5)

  def test_negatives(self):
    self.assertEqual(kth_smallest([0, -5, 3, -1], 2), -1)

  def test_all_equal(self):
    self.assertEqual(kth_smallest([4, 4, 4, 4], 3), 4)

  def test_already_sorted(self):
    self.assertEqual(kth_smallest(list(range(1, 11)), 7), 7)

  def test_reverse_sorted(self):
    self.assertEqual(kth_smallest(list(range(10, 0, -1)), 7), 7)

  def test_larger_mixed(self):
    nums = [12, 3, 5, 7, 4, 19, 26, 3, 8]
    self.assertEqual(kth_smallest(nums, 5), 7)  # sorted: 3,3,4,5,7,...


if __name__ == '__main__':
  unittest.main()
