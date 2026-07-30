import unittest


class TestThreeSum(unittest.TestCase):
  def test_classic_example(self):
    self.assertEqual(
      three_sum([-1, 0, 1, 2, -1, -4], 0),
      [(-1, -1, 2), (-1, 0, 1)],
    )

  def test_all_zeros_single_triplet(self):
    self.assertEqual(three_sum([0, 0, 0, 0], 0), [(0, 0, 0)])

  def test_no_triplet(self):
    self.assertEqual(three_sum([1, 2, 3], 100), [])

  def test_non_zero_target(self):
    self.assertEqual(three_sum([-2, 0, 1, 1, 2], 0), [(-2, 0, 2), (-2, 1, 1)])

  def test_positive_target(self):
    self.assertEqual(three_sum([1, 2, 3, 4, 5], 9), [(1, 3, 5), (2, 3, 4)])

  def test_too_few_elements(self):
    self.assertEqual(three_sum([1, 2], 3), [])
    self.assertEqual(three_sum([], 0), [])

  def test_duplicates_do_not_double_count(self):
    # Many equal values must still yield a single unique triplet per value set.
    self.assertEqual(three_sum([-1, -1, -1, 2, 2, 2], 0), [(-1, -1, 2)])

  def test_all_negative_no_solution(self):
    self.assertEqual(three_sum([-5, -4, -3], 0), [])


if __name__ == '__main__':
  unittest.main()
