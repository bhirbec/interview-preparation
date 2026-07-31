import unittest


class TestMaxNonAdjacentSum(unittest.TestCase):
  def test_classic_example(self):
    self.assertEqual(max_non_adjacent_sum([2, 7, 9, 3, 1]), 12)

  def test_endpoints_beat_middle(self):
    # Taking both 5s requires skipping both middle 1s.
    self.assertEqual(max_non_adjacent_sum([5, 1, 1, 5]), 10)

  def test_course_example(self):
    self.assertEqual(
        max_non_adjacent_sum([17, 14, 5, 4, 82, 12, 1, 34, 1080, 222]), 1185)

  def test_empty(self):
    self.assertEqual(max_non_adjacent_sum([]), 0)

  def test_single(self):
    self.assertEqual(max_non_adjacent_sum([4]), 4)

  def test_two_elements_takes_max(self):
    self.assertEqual(max_non_adjacent_sum([3, 9]), 9)

  def test_all_equal(self):
    # Every other element of six 5s.
    self.assertEqual(max_non_adjacent_sum([5, 5, 5, 5, 5, 5]), 15)

  def test_zeros_allowed(self):
    self.assertEqual(max_non_adjacent_sum([0, 0, 0]), 0)

  def test_large_input_runs_fast(self):
    self.assertEqual(max_non_adjacent_sum([1] * 100000), 50000)


if __name__ == '__main__':
  unittest.main()
