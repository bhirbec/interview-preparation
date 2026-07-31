import unittest


class TestRobotInAGrid(unittest.TestCase):
  def _assert_valid_path(self, matrix, path):
    n, m = len(matrix), len(matrix[0])
    self.assertEqual(path[0], (0, 0))
    self.assertEqual(path[-1], (n - 1, m - 1))
    for (i, j) in path:
      self.assertEqual(matrix[i][j], 0, msg='path steps on blocked cell')
    for (pi, pj), (ci, cj) in zip(path, path[1:]):
      # each step is exactly one move right or one move down
      self.assertIn((ci - pi, cj - pj), [(0, 1), (1, 0)])

  def test_canonical_example(self):
    matrix = [
        [0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 1, 0, 0, 0],
    ]
    self._assert_valid_path(matrix, find_path(matrix))

  def test_simple_path(self):
    matrix = [
        [0, 0],
        [1, 0],
    ]
    self.assertEqual(find_path(matrix), [(0, 0), (0, 1), (1, 1)])

  def test_no_path(self):
    matrix = [
        [0, 1],
        [1, 0],
    ]
    self.assertEqual(find_path(matrix), [])

  def test_single_cell_free(self):
    self.assertEqual(find_path([[0]]), [(0, 0)])

  def test_single_cell_blocked(self):
    self.assertEqual(find_path([[1]]), [])

  def test_start_blocked(self):
    matrix = [
        [1, 0],
        [0, 0],
    ]
    self.assertEqual(find_path(matrix), [])

  def test_goal_blocked(self):
    matrix = [
        [0, 0],
        [0, 1],
    ]
    self.assertEqual(find_path(matrix), [])

  def test_empty_matrix(self):
    self.assertEqual(find_path([]), [])

  def test_empty_row(self):
    self.assertEqual(find_path([[]]), [])

  def test_full_open_grid(self):
    matrix = [[0, 0, 0], [0, 0, 0]]
    self._assert_valid_path(matrix, find_path(matrix))


if __name__ == '__main__':
  unittest.main()
