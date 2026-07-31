import unittest


class TestRecursiveMultiply(unittest.TestCase):
  def test_multiply_by_zero(self):
    self.assertEqual(multiply(0, 5), 0)
    self.assertEqual(multiply(5, 0), 0)
    self.assertEqual(multiply(0, 0), 0)

  def test_multiply_by_one(self):
    self.assertEqual(multiply(7, 1), 7)
    self.assertEqual(multiply(1, 7), 7)

  def test_small_products(self):
    self.assertEqual(multiply(3, 4), 12)
    self.assertEqual(multiply(9, 9), 81)
    self.assertEqual(multiply(6, 7), 42)

  def test_matches_builtin_over_range(self):
    for a in range(0, 40):
      for b in range(0, 40):
        self.assertEqual(multiply(a, b), a * b)

  def test_large_values(self):
    self.assertEqual(multiply(123, 123312), 123 * 123312)


if __name__ == '__main__':
  unittest.main()
