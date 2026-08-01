import unittest


class TestSortedSquares(unittest.TestCase):
  def test_example(self):
    self.assertEqual(sorted_squares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])

  def test_duplicate_squares(self):
    self.assertEqual(sorted_squares([-7, -3, 2, 3, 11]), [4, 9, 9, 49, 121])

  def test_all_positive(self):
    self.assertEqual(sorted_squares([1, 2, 3]), [1, 4, 9])

  def test_all_negative(self):
    self.assertEqual(sorted_squares([-5, -3, -1]), [1, 9, 25])

  def test_empty(self):
    self.assertEqual(sorted_squares([]), [])

  def test_single_element(self):
    self.assertEqual(sorted_squares([-2]), [4])

  def test_repeated_values(self):
    self.assertEqual(sorted_squares([-2, -2, 2, 2]), [4, 4, 4, 4])

  def test_zeros(self):
    self.assertEqual(sorted_squares([0, 0]), [0, 0])

  def test_matches_sorting(self):
    cases = [
        [-9, -4, -2, 0, 1, 6, 8],
        [-1, 0, 1],
        [-10000, 10000],
        [3],
    ]
    for nums in cases:
      self.assertEqual(sorted_squares(nums), sorted(n * n for n in nums),
                       str(nums))

  def test_input_is_not_mutated(self):
    nums = [-3, -1, 4]
    sorted_squares(nums)
    self.assertEqual(nums, [-3, -1, 4])


if __name__ == '__main__':
  unittest.main()
