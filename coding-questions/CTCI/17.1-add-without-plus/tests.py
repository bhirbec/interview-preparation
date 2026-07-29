import unittest


class TestAdd(unittest.TestCase):
  def test_positive(self):
    self.assertEqual(add(5, 3), 8)
    self.assertEqual(add(123, 877), 1000)

  def test_zero(self):
    self.assertEqual(add(0, 0), 0)
    self.assertEqual(add(7, 0), 7)
    self.assertEqual(add(0, 42), 42)

  def test_negative_and_positive(self):
    self.assertEqual(add(-3, 5), 2)
    self.assertEqual(add(5, -3), 2)
    self.assertEqual(add(-10, 4), -6)

  def test_both_negative(self):
    self.assertEqual(add(-4, -6), -10)
    self.assertEqual(add(-1, -1), -2)

  def test_result_zero_from_opposites(self):
    self.assertEqual(add(9, -9), 0)

  def test_exhaustive_small_range(self):
    for a in range(-50, 51):
      for b in range(-50, 51):
        self.assertEqual(add(a, b), a + b)


if __name__ == '__main__':
  unittest.main()
