import unittest


class TestMinMultiplications(unittest.TestCase):
  def test_two_matrices(self):
    self.assertEqual(min_multiplications([10, 20, 30]), 6000)

  def test_three_matrices_order_matters(self):
    self.assertEqual(min_multiplications([10, 20, 30, 40]), 18000)

  def test_classic_clrs_chain(self):
    self.assertEqual(min_multiplications([30, 35, 15, 5, 10, 20, 25]), 15125)

  def test_single_matrix(self):
    self.assertEqual(min_multiplications([5, 10]), 0)

  def test_skinny_middle_matrix_first(self):
    # Collapsing through the 1-wide middle is drastically cheaper.
    self.assertEqual(min_multiplications([100, 1, 100, 1]), 200)

  def test_unit_dimensions(self):
    self.assertEqual(min_multiplications([1, 1, 1, 1]), 2)


if __name__ == '__main__':
  unittest.main()
