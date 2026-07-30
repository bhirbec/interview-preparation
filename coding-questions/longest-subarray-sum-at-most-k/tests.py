import unittest


class TestLongestSubarrayAtMostK(unittest.TestCase):
  def test_example_mixed(self):
    self.assertEqual(longest_subarray_at_most_k([3, 1, 2, 3, 4], 3), 2)

  def test_all_ones(self):
    self.assertEqual(longest_subarray_at_most_k([1, 1, 1, 1], 2), 2)

  def test_no_element_fits(self):
    self.assertEqual(longest_subarray_at_most_k([5, 6, 7], 4), 0)

  def test_whole_array_fits(self):
    self.assertEqual(longest_subarray_at_most_k([1, 2, 3], 100), 3)

  def test_single_element_equal_to_k(self):
    self.assertEqual(longest_subarray_at_most_k([2], 2), 1)

  def test_single_element_exceeds_k(self):
    self.assertEqual(longest_subarray_at_most_k([5], 2), 0)

  def test_empty_array(self):
    self.assertEqual(longest_subarray_at_most_k([], 5), 0)

  def test_k_zero_with_positive_values(self):
    # No non-empty subarray of positive values can sum to 0.
    self.assertEqual(longest_subarray_at_most_k([1, 2, 3], 0), 0)

  def test_best_window_at_the_end(self):
    self.assertEqual(longest_subarray_at_most_k([9, 9, 1, 1, 1], 3), 3)

  def test_best_window_at_the_start(self):
    self.assertEqual(longest_subarray_at_most_k([1, 1, 1, 9, 9], 3), 3)

  def test_all_identical_all_fit(self):
    self.assertEqual(longest_subarray_at_most_k([2, 2, 2, 2], 8), 4)

  def test_exact_sum_prefers_longer(self):
    self.assertEqual(longest_subarray_at_most_k([1, 1, 1, 1, 1], 3), 3)


if __name__ == '__main__':
  unittest.main()
