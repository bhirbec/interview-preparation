import unittest


class TestProductExceptSelf(unittest.TestCase):
  def test_empty(self):
    self.assertEqual(product_except_self([]), [])

  def test_single_element(self):
    self.assertEqual(product_except_self([7]), [1])

  def test_basic(self):
    self.assertEqual(product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])

  def test_negatives(self):
    res = product_except_self([-2, 12, 3, -6, 21])
    self.assertEqual(res[0], 12 * 3 * -6 * 21)
    self.assertEqual(res[1], -2 * 3 * -6 * 21)
    self.assertEqual(res[4], -2 * 12 * 3 * -6)
    self.assertEqual(res, [-4536, 756, 3024, -1512, 432])

  def test_single_zero(self):
    self.assertEqual(product_except_self([0, 4, 3]), [12, 0, 0])

  def test_multiple_zeros(self):
    self.assertEqual(product_except_self([0, 0, 5]), [0, 0, 0])

  def test_two_elements(self):
    self.assertEqual(product_except_self([3, 7]), [7, 3])

  def test_ones(self):
    self.assertEqual(product_except_self([1, 1, 1, 1]), [1, 1, 1, 1])

  def test_no_division_used(self):
    # A zero in the array would raise ZeroDivisionError for a division-based
    # solution; a correct one handles it cleanly.
    self.assertEqual(product_except_self([5, 0]), [0, 5])


if __name__ == '__main__':
  unittest.main()
