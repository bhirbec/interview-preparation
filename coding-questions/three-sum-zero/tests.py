import unittest


class TestThreeSumZero(unittest.TestCase):
  def test_example(self):
    nums = [2, 3, 1, -2, -1, 0, 2, -3, 0]
    self.assertEqual(three_sum_zero(nums),
                     [[-3, 0, 3], [-3, 1, 2], [-2, -1, 3], [-2, 0, 2],
                      [-1, 0, 1]])

  def test_empty(self):
    self.assertEqual(three_sum_zero([]), [])

  def test_too_few_elements(self):
    self.assertEqual(three_sum_zero([1, -1]), [])

  def test_no_triplet(self):
    self.assertEqual(three_sum_zero([1, 2, 3, 4]), [])

  def test_all_zeros(self):
    self.assertEqual(three_sum_zero([0, 0, 0, 0]), [[0, 0, 0]])

  def test_single_triplet(self):
    self.assertEqual(three_sum_zero([-1, 0, 1]), [[-1, 0, 1]])

  def test_duplicate_values_deduped(self):
    self.assertEqual(three_sum_zero([-1, -1, 2, 2, 0, 0, 0]),
                     [[-1, -1, 2], [0, 0, 0]])

  def test_no_zero_present(self):
    self.assertEqual(three_sum_zero([-4, 1, 3, 5]), [[-4, 1, 3]])


if __name__ == '__main__':
  unittest.main()
