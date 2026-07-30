import unittest


class TestTrapWater(unittest.TestCase):
  def test_example_one(self):
    self.assertEqual(trap_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)

  def test_example_two(self):
    self.assertEqual(trap_water([4, 2, 0, 3, 2, 5]), 9)

  def test_empty(self):
    self.assertEqual(trap_water([]), 0)

  def test_single_bar(self):
    self.assertEqual(trap_water([7]), 0)

  def test_two_bars(self):
    self.assertEqual(trap_water([5, 3]), 0)

  def test_flat(self):
    self.assertEqual(trap_water([3, 3, 3]), 0)

  def test_monotonic_decreasing(self):
    self.assertEqual(trap_water([5, 4, 3, 2, 1]), 0)

  def test_monotonic_increasing(self):
    self.assertEqual(trap_water([1, 2, 3, 4, 5]), 0)

  def test_single_basin(self):
    self.assertEqual(trap_water([3, 0, 3]), 3)

  def test_valley_with_zeros(self):
    self.assertEqual(trap_water([2, 0, 2, 0, 2]), 4)


if __name__ == '__main__':
  unittest.main()
