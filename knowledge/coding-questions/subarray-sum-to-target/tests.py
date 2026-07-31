import unittest


class TestFindSubarrayWithSum(unittest.TestCase):
  def test_example_middle_window(self):
    self.assertEqual(find_subarray_with_sum([1, 5, 10, 3], 18), (1, 3))

  def test_example_tail_window(self):
    self.assertEqual(find_subarray_with_sum([1, 2, 3, 4], 9), (1, 3))

  def test_single_element_match(self):
    self.assertEqual(find_subarray_with_sum([5], 5), (0, 0))

  def test_single_element_no_match(self):
    self.assertIsNone(find_subarray_with_sum([5], 3))

  def test_no_subarray(self):
    self.assertIsNone(find_subarray_with_sum([1, 2, 3], 7))

  def test_window_at_start(self):
    self.assertEqual(find_subarray_with_sum([2, 4, 6], 6), (0, 1))

  def test_whole_array(self):
    self.assertEqual(find_subarray_with_sum([1, 2, 3, 4], 10), (0, 3))

  def test_single_element_in_middle(self):
    self.assertEqual(find_subarray_with_sum([3, 5, 2], 5), (1, 1))

  def test_smallest_start_index_wins(self):
    # Both (0,2) and (2,4) sum to 6; the earlier start is returned.
    self.assertEqual(find_subarray_with_sum([1, 2, 3, 3, 3], 6), (0, 2))


if __name__ == '__main__':
  unittest.main()
