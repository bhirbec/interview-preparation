import unittest


class TestMaxSubarray(unittest.TestCase):
  def test_canonical_example(self):
    self.assertEqual(max_subarray([-1, 2, 3, -3, 2, 3, 4, -4]), (11, 1, 6))

  def test_kadane_example(self):
    self.assertEqual(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), (6, 3, 6))

  def test_single_positive(self):
    self.assertEqual(max_subarray([5]), (5, 0, 0))

  def test_all_negative_returns_zero(self):
    # No non-empty subarray beats the empty one, so the max sum is 0.
    # (The returned indices are meaningless in this case and not asserted.)
    self.assertEqual(max_subarray([-1, -2, -3])[0], 0)

  def test_empty_array(self):
    self.assertEqual(max_subarray([]), (0, 0, 0))

  def test_all_positive(self):
    self.assertEqual(max_subarray([1, 2, 3, 4]), (10, 0, 3))

  def test_leading_negative(self):
    self.assertEqual(max_subarray([-5, 4]), (4, 1, 1))

  def test_best_subarray_at_end(self):
    self.assertEqual(max_subarray([1, -5, 2, 6]), (8, 2, 3))

  def test_single_negative(self):
    self.assertEqual(max_subarray([-7])[0], 0)

  def test_zeros_and_positives(self):
    self.assertEqual(max_subarray([0, 0, 3, 0]), (3, 0, 2))


if __name__ == '__main__':
  unittest.main()
