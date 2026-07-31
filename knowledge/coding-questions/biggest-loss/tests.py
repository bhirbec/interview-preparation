import unittest


class TestMaxLoss(unittest.TestCase):
  def test_glassdoor_example(self):
    prices = [23, 24, 27, 532, 14, 12, 17, 121, 24, 1344, 0]
    self.assertEqual(max_loss(prices), 1344)

  def test_only_rises(self):
    self.assertEqual(max_loss([1, 2, 3, 4]), 0)

  def test_loss_in_the_middle(self):
    self.assertEqual(max_loss([10, 7, 5, 8, 11, 2, 6]), 9)

  def test_single_price(self):
    self.assertEqual(max_loss([5]), 0)

  def test_empty(self):
    self.assertEqual(max_loss([]), 0)

  def test_two_prices_drop(self):
    self.assertEqual(max_loss([9, 2]), 7)

  def test_flat_prices(self):
    self.assertEqual(max_loss([4, 4, 4, 4]), 0)

  def test_biggest_drop_is_first_pair(self):
    self.assertEqual(max_loss([100, 1, 50, 60]), 99)


if __name__ == '__main__':
  unittest.main()
