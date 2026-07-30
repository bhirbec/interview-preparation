import unittest


class TestSpiralMatrix(unittest.TestCase):
  def test_one(self):
    self.assertEqual(spiral_matrix(1), [[1]])

  def test_two(self):
    self.assertEqual(spiral_matrix(2), [[1, 2],
                                        [4, 3]])

  def test_three_odd_has_center(self):
    self.assertEqual(spiral_matrix(3), [[1, 2, 3],
                                        [8, 9, 4],
                                        [7, 6, 5]])

  def test_four_even(self):
    self.assertEqual(spiral_matrix(4), [[1, 2, 3, 4],
                                        [12, 13, 14, 5],
                                        [11, 16, 15, 6],
                                        [10, 9, 8, 7]])

  def test_all_values_present_once(self):
    n = 5
    flat = sorted(v for row in spiral_matrix(n) for v in row)
    self.assertEqual(flat, list(range(1, n * n + 1)))

  def test_dimensions(self):
    m = spiral_matrix(7)
    self.assertEqual(len(m), 7)
    self.assertTrue(all(len(row) == 7 for row in m))


if __name__ == '__main__':
  unittest.main()
