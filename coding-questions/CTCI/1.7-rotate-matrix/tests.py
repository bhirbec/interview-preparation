import unittest


class TestRotate(unittest.TestCase):
  def test_two_by_two(self):
    self.assertEqual(rotate([[1, 2], [3, 4]]), [[2, 4], [1, 3]])

  def test_three_by_three(self):
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    self.assertEqual(rotate(mat), [[3, 6, 9], [2, 5, 8], [1, 4, 7]])

  def test_single_element(self):
    self.assertEqual(rotate([[1]]), [[1]])

  def test_empty(self):
    self.assertEqual(rotate([]), [])

  def test_rotates_in_place(self):
    mat = [[1, 2], [3, 4]]
    result = rotate(mat)
    self.assertIs(result, mat)  # same object, mutated in place

  def test_four_by_four(self):
    mat = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    expected = [
        [4, 8, 12, 16],
        [3, 7, 11, 15],
        [2, 6, 10, 14],
        [1, 5, 9, 13],
    ]
    self.assertEqual(rotate(mat), expected)


if __name__ == '__main__':
  unittest.main()
