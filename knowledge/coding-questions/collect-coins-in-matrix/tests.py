import unittest


class TestMaxCoinsCollected(unittest.TestCase):
  def test_empty(self):
    self.assertEqual(max_coins_collected([]), 0)

  def test_single_coin(self):
    self.assertEqual(max_coins_collected([(5, 7)]), 1)

  def test_full_chain(self):
    self.assertEqual(max_coins_collected([(1, 1), (2, 2), (3, 3)]), 3)

  def test_no_two_compatible(self):
    self.assertEqual(max_coins_collected([(1, 3), (2, 2), (3, 1)]), 1)

  def test_shared_x_conflicts(self):
    self.assertEqual(max_coins_collected([(1, 1), (1, 2), (2, 3)]), 2)

  def test_shared_y_conflicts(self):
    # (1, 5) and (3, 5) share y, so at most one of them is on any chain.
    self.assertEqual(max_coins_collected([(1, 5), (3, 5), (2, 6)]), 2)

  def test_unsorted_input(self):
    coins = [(8, 9), (2, 4), (1, 8), (3, 5), (3, 7)]
    # (2,4) -> (3,5) -> (8,9) is a length-3 chain; the two x=3 coins conflict.
    self.assertEqual(max_coins_collected(coins), 3)

  def test_reverse_sorted_on_y(self):
    self.assertEqual(max_coins_collected([(1, 4), (2, 3), (3, 2), (4, 1)]), 1)

  def test_all_identical(self):
    self.assertEqual(max_coins_collected([(2, 2), (2, 2), (2, 2)]), 1)


if __name__ == '__main__':
  unittest.main()
