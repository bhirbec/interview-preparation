import unittest


class TestGoodNumbers(unittest.TestCase):
  def test_none_below_1729(self):
    self.assertEqual(good_numbers(1000), [])

  def test_first_taxicab(self):
    self.assertEqual(good_numbers(1729), [1729])

  def test_two_taxicabs(self):
    self.assertEqual(good_numbers(4200), [1729, 4104])

  def test_zero(self):
    self.assertEqual(good_numbers(0), [])

  def test_just_below_boundary(self):
    self.assertEqual(good_numbers(1728), [])

  def test_exact_boundary_inclusive(self):
    # n equal to a good number includes it.
    self.assertEqual(good_numbers(1729), [1729])

  def test_small_n(self):
    self.assertEqual(good_numbers(1), [])


if __name__ == '__main__':
  unittest.main()
