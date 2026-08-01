import unittest


class TestDailyTemperatures(unittest.TestCase):
  def test_example(self):
    self.assertEqual(
        daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]),
        [1, 1, 4, 2, 1, 1, 0, 0])

  def test_strictly_increasing(self):
    self.assertEqual(daily_temperatures([30, 40, 50, 60]), [1, 1, 1, 0])

  def test_strictly_decreasing(self):
    self.assertEqual(daily_temperatures([60, 50, 40, 30]), [0, 0, 0, 0])

  def test_single_day(self):
    self.assertEqual(daily_temperatures([50]), [0])

  def test_all_equal_never_strictly_warmer(self):
    self.assertEqual(daily_temperatures([70, 70, 70]), [0, 0, 0])

  def test_warmer_day_far_in_the_future(self):
    self.assertEqual(daily_temperatures([40, 35, 32, 30, 50]), [4, 3, 2, 1, 0])

  def test_valley_then_peak(self):
    self.assertEqual(daily_temperatures([50, 30, 40, 60]), [3, 1, 1, 0])

  def test_boundary_temperatures(self):
    self.assertEqual(daily_temperatures([30, 100, 30]), [1, 0, 0])


if __name__ == '__main__':
  unittest.main()
