import unittest


class TestLengthOfLis(unittest.TestCase):
  def test_leetcode_example(self):
    self.assertEqual(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)

  def test_readme_example(self):
    self.assertEqual(length_of_lis([3, 2, 6, 4, 5, 1]), 3)

  def test_with_repeats_between_runs(self):
    self.assertEqual(length_of_lis([0, 1, 0, 3, 2, 3]), 4)

  def test_all_equal_is_strict(self):
    self.assertEqual(length_of_lis([7, 7, 7, 7, 7]), 1)

  def test_empty(self):
    self.assertEqual(length_of_lis([]), 0)

  def test_single_element(self):
    self.assertEqual(length_of_lis([42]), 1)

  def test_two_increasing(self):
    self.assertEqual(length_of_lis([1, 2]), 2)

  def test_two_decreasing(self):
    self.assertEqual(length_of_lis([2, 1]), 1)

  def test_already_sorted(self):
    self.assertEqual(length_of_lis([1, 2, 3, 4, 5]), 5)

  def test_strictly_decreasing(self):
    self.assertEqual(length_of_lis([5, 4, 3, 2, 1]), 1)

  def test_negatives(self):
    self.assertEqual(length_of_lis([-8, -2, -3, -1]), 3)

  def test_duplicates_do_not_count(self):
    # 1, 2, 3, 4 is length 4; the duplicate 3 cannot extend a 3.
    self.assertEqual(length_of_lis([1, 3, 2, 3, 4]), 4)

  def test_best_run_at_end(self):
    self.assertEqual(length_of_lis([9, 8, 1, 2, 3, 4]), 4)


if __name__ == '__main__':
  unittest.main()
