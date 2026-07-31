import unittest


class TestFindBestPath(unittest.TestCase):
  def test_documented_example(self):
    matrix = [
      [4, 5, 9],
      [8, 1, 3],
      [2, 6, 7],
    ]
    self.assertEqual(find_best_path(matrix), [4, 5, 1, 3, 7])

  def test_single_cell(self):
    self.assertEqual(find_best_path([[1]]), [1])

  def test_single_row(self):
    self.assertEqual(find_best_path([[1, 2, 3, 4]]), [1, 2, 3, 4])

  def test_single_column(self):
    self.assertEqual(find_best_path([[1], [2], [3], [4]]), [1, 2, 3, 4])

  def test_two_by_two(self):
    # Paths: [1,2,4] via top-right, [1,3,4] via bottom-left. [1,2,4] wins.
    matrix = [
      [1, 2],
      [3, 4],
    ]
    self.assertEqual(find_best_path(matrix), [1, 2, 4])

  def test_smallest_value_forces_a_turn(self):
    matrix = [
      [1, 9, 8],
      [7, 2, 6],
      [5, 4, 3],
    ]
    # Best sorted path is [1,2,3,4,7]: reach 2 at (1,1) via 7, then 4 then 3.
    self.assertEqual(find_best_path(matrix), [1, 7, 2, 4, 3])

  def test_result_length_matches_path(self):
    matrix = [
      [7, 4, 6, 10],
      [8, 1, 9, 11],
      [3, 5, 2, 13],
      [14, 15, 16, 12],
    ]
    # A path across a 4x4 grid visits R + C - 1 = 7 cells.
    self.assertEqual(len(find_best_path(matrix)), 7)

  def test_input_not_mutated(self):
    matrix = [
      [4, 5, 9],
      [8, 1, 3],
      [2, 6, 7],
    ]
    find_best_path(matrix)
    self.assertEqual(matrix, [[4, 5, 9], [8, 1, 3], [2, 6, 7]])


if __name__ == '__main__':
  unittest.main()
