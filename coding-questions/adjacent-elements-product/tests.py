import unittest


class TestAdjacentElementsProduct(unittest.TestCase):
  def test_mixed_signs(self):
    self.assertEqual(adjacent_elements_product([3, 6, -2, -5, 7, 3]), 21)

  def test_all_positive(self):
    self.assertEqual(adjacent_elements_product([5, 1, 2, 3, 1, 40]), 40)

  def test_two_negatives(self):
    self.assertEqual(adjacent_elements_product([-1, -2]), 2)

  def test_negative_tail(self):
    self.assertEqual(adjacent_elements_product([9, 5, 10, 2, 24, -1, -48]), 50)

  def test_zeros(self):
    self.assertEqual(adjacent_elements_product([1, 0, 1, 0, 1000]), 0)

  def test_minimum_length(self):
    self.assertEqual(adjacent_elements_product([4, 7]), 28)

  def test_all_negative(self):
    self.assertEqual(adjacent_elements_product([-6, -1, -3, -4]), 12)

  def test_best_is_first_pair(self):
    self.assertEqual(adjacent_elements_product([100, 100, 1, 2]), 10000)


if __name__ == '__main__':
  unittest.main()
