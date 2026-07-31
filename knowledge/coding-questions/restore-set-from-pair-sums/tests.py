import unittest
from itertools import combinations


class TestRestoreSet(unittest.TestCase):
  def check(self, sums, n):
    result = restore_set(sums)
    self.assertEqual(len(result), n)
    produced = sorted(a + b for a, b in combinations(result, 2))
    for got, want in zip(produced, sorted(sums)):
      self.assertAlmostEqual(got, want, places=6)

  def test_three_numbers_smallest_case(self):
    self.check([3, 4, 5], 3)

  def test_ambiguous_case_accepts_any_valid_answer(self):
    # Both {1, 2, 3, 17} and {-5.5, 8.5, 9.5, 10.5} produce these sums.
    self.check([3, 4, 5, 18, 19, 20], 4)

  def test_all_equal_values(self):
    self.assertEqual(restore_set([10, 10, 10]), [5, 5, 5])

  def test_consecutive_with_duplicate_sums(self):
    # X = {1, 2, 3, 4} -> sums contain 5 twice.
    self.check([3, 4, 5, 5, 6, 7], 4)

  def test_negative_values(self):
    # X = {-3, 0, 4, 9, 12}
    self.check([-3, 1, 4, 6, 9, 9, 12, 13, 16, 21], 5)

  def test_five_values_round_trip(self):
    # X = {2, 7, 11, 15, 20}
    x = [2, 7, 11, 15, 20]
    sums = [a + b for a, b in combinations(x, 2)]
    self.check(sums, 5)

  def test_shuffled_input_order(self):
    self.check([20, 3, 19, 4, 18, 5], 4)


if __name__ == '__main__':
  unittest.main()
