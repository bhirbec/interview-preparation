import unittest


class TestFindMaxAverage(unittest.TestCase):
  def test_example(self):
    self.assertAlmostEqual(
        find_max_average([1, 12, -5, -6, 50, 3], 4), 12.75, places=5)

  def test_single_element(self):
    self.assertAlmostEqual(find_max_average([5], 1), 5.0, places=5)

  def test_window_of_one_picks_the_max(self):
    self.assertAlmostEqual(find_max_average([0, 4, 0, 3, 2], 1), 4.0, places=5)

  def test_window_is_whole_array(self):
    self.assertAlmostEqual(find_max_average([1, 2, 3, 4], 4), 2.5, places=5)

  def test_all_negative(self):
    self.assertAlmostEqual(find_max_average([-1, -2, -3], 2), -1.5, places=5)

  def test_best_window_at_the_end(self):
    self.assertAlmostEqual(find_max_average([-5, -5, 1, 9], 2), 5.0, places=5)

  def test_best_window_at_the_start(self):
    self.assertAlmostEqual(find_max_average([9, 1, -5, -5], 2), 5.0, places=5)

  def test_plateau_of_equal_values(self):
    self.assertAlmostEqual(find_max_average([3, 3, 3, 3], 2), 3.0, places=5)

  def test_returns_a_float_not_an_int(self):
    self.assertIsInstance(find_max_average([2, 2], 2), float)


if __name__ == '__main__':
  unittest.main()
