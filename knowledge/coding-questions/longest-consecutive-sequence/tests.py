import unittest


class TestLongestConsecutive(unittest.TestCase):
  def test_example(self):
    self.assertEqual(longest_consecutive([100, 4, 200, 1, 3, 2]), 4)

  def test_longer_run_with_duplicate(self):
    self.assertEqual(
        longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)

  def test_all_duplicates(self):
    self.assertEqual(longest_consecutive([1, 1, 1]), 1)

  def test_empty(self):
    self.assertEqual(longest_consecutive([]), 0)

  def test_single_element(self):
    self.assertEqual(longest_consecutive([42]), 1)

  def test_no_consecutive_values(self):
    self.assertEqual(longest_consecutive([10, 30, 20]), 1)

  def test_negative_values(self):
    self.assertEqual(longest_consecutive([-3, -2, -1, 5, 7]), 3)

  def test_run_crossing_zero(self):
    self.assertEqual(longest_consecutive([1, -1, 0, 2, -2]), 5)

  def test_two_runs_longest_wins(self):
    self.assertEqual(longest_consecutive([1, 2, 3, 10, 11, 12, 13]), 4)

  def test_already_sorted(self):
    self.assertEqual(longest_consecutive([1, 2, 3, 4, 5]), 5)


if __name__ == '__main__':
  unittest.main()
