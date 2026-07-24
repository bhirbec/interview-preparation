# Matrix Elements Sum
#
# Difficulty: easy
# Tags: #matrix #array
#
# You are given a matrix of integers `matrix` where matrix[i][j] is the price of
# the room on floor i, column j of a hotel (row 0 is the top floor). A price of 0
# means that room is unavailable, and — because guests are superstitious — every
# room directly below an unavailable room, in the same column, is also considered
# unavailable, regardless of its own price.
#
# Return the total price of all available rooms: for each column, add up prices
# from the top floor downward, stopping as soon as you reach a 0 in that column.
#
# Constraints:
#   - 1 <= len(matrix), len(matrix[0]) <= 100
#   - 0 <= matrix[i][j] <= 10000
#   - every row has the same number of columns
#
# Examples:
#   [[0, 1, 1, 2],       col sums: 0 | 1+5 | 1 | 2   -> 9
#    [0, 5, 0, 0],
#    [2, 0, 3, 3]]
#
#   [[1, 1, 1, 0],       col sums: 1 | 1+5+1 | 1 | 0 -> 9
#    [0, 5, 0, 1],
#    [2, 1, 3, 10]]
#
#   [[0]]                col sums: 0                  -> 0
#   [[1, 5], [3, 2]]     col sums: 1+3 | 5+2          -> 11
#
# Approach: walk each column top-to-bottom, accumulating prices until a 0 breaks
# the column.

import unittest


def matrix_elements_sum(matrix):
  total = 0
  nb_rows = len(matrix)
  nb_cols = len(matrix[0])
  for j in range(nb_cols):
    for i in range(nb_rows):
      cost = matrix[i][j]
      if cost == 0:
        break
      total += cost

  return total


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
