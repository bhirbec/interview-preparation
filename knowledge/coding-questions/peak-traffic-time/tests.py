import unittest


class TestPeakTrafficTime(unittest.TestCase):
  def test_log_example(self):
    self.assertEqual(peak_traffic_time([(0, 10), (3, 15), (8, 29), (4, 14)]), 8)

  def test_disjoint_sessions_peak_at_first(self):
    self.assertEqual(peak_traffic_time([(0, 1), (2, 3)]), 0)

  def test_touching_intervals_do_not_overlap(self):
    self.assertEqual(peak_traffic_time([(0, 5), (5, 10)]), 0)

  def test_single_session(self):
    self.assertEqual(peak_traffic_time([(7, 20)]), 7)

  def test_nested_sessions(self):
    self.assertEqual(peak_traffic_time([(0, 10), (2, 8), (3, 5)]), 3)

  def test_tie_returns_earliest_peak(self):
    # Two separate periods reach concurrency 2; the first starts at 1.
    self.assertEqual(
        peak_traffic_time([(0, 3), (1, 2), (10, 13), (11, 12)]), 1)

  def test_unsorted_input(self):
    self.assertEqual(peak_traffic_time([(8, 29), (0, 10), (4, 14), (3, 15)]), 8)

  def test_identical_sessions(self):
    self.assertEqual(peak_traffic_time([(5, 9), (5, 9), (5, 9)]), 5)


if __name__ == '__main__':
  unittest.main()
