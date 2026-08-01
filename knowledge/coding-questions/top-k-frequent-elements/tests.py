import unittest


class TestTopKFrequent(unittest.TestCase):
  def test_example(self):
    self.assertEqual(top_k_frequent([1, 1, 1, 2, 2, 3], 2), [1, 2])

  def test_single_element(self):
    self.assertEqual(top_k_frequent([1], 1), [1])

  def test_tie_prefers_smaller_value(self):
    self.assertEqual(top_k_frequent([4, 4, 5, 5, 6], 2), [4, 5])

  def test_k_is_one(self):
    self.assertEqual(top_k_frequent([3, 0, 1, 0], 1), [0])

  def test_k_covers_every_distinct_value(self):
    self.assertEqual(top_k_frequent([5, 5, 4, 4, 4, 6], 3), [4, 5, 6])

  def test_all_values_distinct(self):
    self.assertEqual(top_k_frequent([7, 8, 9], 2), [7, 8])

  def test_negative_values(self):
    self.assertEqual(top_k_frequent([-1, -1, -2, -2, -2, 5], 2), [-2, -1])

  def test_all_identical(self):
    self.assertEqual(top_k_frequent([2, 2, 2, 2], 1), [2])

  def test_strict_frequency_order(self):
    nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
    self.assertEqual(top_k_frequent(nums, 4), [4, 3, 2, 1])


if __name__ == '__main__':
  unittest.main()
