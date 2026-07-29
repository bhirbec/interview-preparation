import unittest

CANONICAL = [15, 16, 19, 20, 25, 1, 3, 4, 5, 7, 10, 14]


class TestSearchInRotatedArray(unittest.TestCase):
  def test_find_value_in_low_run(self):
    self.assertEqual(find(CANONICAL, 5), 8)

  def test_find_value_in_high_run(self):
    # This is the case the original buggy version missed.
    self.assertEqual(find(CANONICAL, 15), 0)
    self.assertEqual(find(CANONICAL, 25), 4)

  def test_find_every_element(self):
    for i, v in enumerate(CANONICAL):
      self.assertEqual(find(CANONICAL, v), i, msg=f'value {v}')

  def test_missing_value(self):
    self.assertIsNone(find(CANONICAL, 100))
    self.assertIsNone(find(CANONICAL, 2))
    self.assertIsNone(find(CANONICAL, -5))

  def test_not_rotated(self):
    arr = [1, 2, 3, 4, 5]
    for i, v in enumerate(arr):
      self.assertEqual(find(arr, v), i)
    self.assertIsNone(find(arr, 6))

  def test_reverse_boundaries(self):
    # Rotation such that the pivot sits near either end.
    self.assertEqual(find([2, 3, 4, 5, 1], 1), 4)   # pivot at last index
    self.assertEqual(find([5, 1, 2, 3, 4], 5), 0)   # pivot right after index 0
    self.assertEqual(find([5, 1, 2, 3, 4], 1), 1)

  def test_two_elements(self):
    self.assertEqual(find([1, 2], 1), 0)
    self.assertEqual(find([1, 2], 2), 1)
    self.assertEqual(find([2, 1], 1), 1)
    self.assertEqual(find([2, 1], 2), 0)

  def test_single_element(self):
    self.assertEqual(find([5], 5), 0)
    self.assertIsNone(find([5], 3))

  def test_empty(self):
    self.assertIsNone(find([], 1))


if __name__ == '__main__':
  unittest.main()
