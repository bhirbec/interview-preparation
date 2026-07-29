import unittest


class TestMakeArrayConsecutive(unittest.TestCase):
  def test_example(self):
    self.assertEqual(make_array_consecutive([6, 2, 3, 8]), 3)

  def test_two_element_gap(self):
    self.assertEqual(make_array_consecutive([0, 3]), 2)

  def test_already_consecutive(self):
    self.assertEqual(make_array_consecutive([5, 4, 6]), 0)

  def test_single_statue(self):
    self.assertEqual(make_array_consecutive([6]), 0)

  def test_unsorted_input(self):
    self.assertEqual(make_array_consecutive([8, 3, 6, 2]), 3)

  def test_large_gap(self):
    self.assertEqual(make_array_consecutive([1, 10]), 8)

  def test_starts_at_zero(self):
    self.assertEqual(make_array_consecutive([0]), 0)

  def test_outlier_high_value(self):
    self.assertEqual(make_array_consecutive([6, 2, 3, 8, 15]), 9)


if __name__ == '__main__':
  unittest.main()
