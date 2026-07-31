import unittest


class TestMatrixElementsSum(unittest.TestCase):
  def test_example_one(self):
    matrix = [
        [0, 1, 1, 2],
        [0, 5, 0, 0],
        [2, 0, 3, 3],
    ]
    self.assertEqual(matrix_elements_sum(matrix), 9)

  def test_example_two(self):
    matrix = [
        [1, 1, 1, 0],
        [0, 5, 0, 1],
        [2, 1, 3, 10],
    ]
    self.assertEqual(matrix_elements_sum(matrix), 9)

  def test_single_zero(self):
    self.assertEqual(matrix_elements_sum([[0]]), 0)

  def test_no_haunted_rooms(self):
    self.assertEqual(matrix_elements_sum([[1, 5], [3, 2]]), 11)

  def test_single_row(self):
    self.assertEqual(matrix_elements_sum([[1, 0, 2, 3]]), 6)

  def test_single_column(self):
    self.assertEqual(matrix_elements_sum([[4], [0], [9]]), 4)

  def test_all_zeros(self):
    self.assertEqual(matrix_elements_sum([[0, 0], [0, 0]]), 0)

  def test_top_row_zero_blocks_column(self):
    self.assertEqual(matrix_elements_sum([[0, 3], [7, 4]]), 7)


if __name__ == '__main__':
  unittest.main()
