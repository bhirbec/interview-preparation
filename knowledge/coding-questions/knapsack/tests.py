import unittest


class TestKnapsack(unittest.TestCase):
  def test_canonical_example(self):
    self.assertEqual(knapsack([(1, 7), (4, 2), (5, 4), (7, 5)], 9), 12)

  def test_greedy_by_density_fails(self):
    # Density-greedy takes (60,10) first and ends at 180; optimal skips it.
    self.assertEqual(knapsack([(60, 10), (100, 20), (120, 30)], 50), 220)

  def test_no_items(self):
    self.assertEqual(knapsack([], 10), 0)

  def test_zero_capacity(self):
    self.assertEqual(knapsack([(5, 1)], 0), 0)

  def test_single_item_fits(self):
    self.assertEqual(knapsack([(8, 3)], 3), 8)

  def test_single_item_too_heavy(self):
    self.assertEqual(knapsack([(8, 4)], 3), 0)

  def test_everything_fits(self):
    self.assertEqual(knapsack([(2, 1), (3, 1), (4, 1)], 10), 9)

  def test_exact_capacity_split(self):
    # Must pick the pair summing exactly to the capacity.
    self.assertEqual(knapsack([(10, 6), (7, 3), (8, 3)], 6), 15)


if __name__ == '__main__':
  unittest.main()
