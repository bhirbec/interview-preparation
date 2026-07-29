# Robot in a Grid
# Difficulty: medium
# Tags: #matrix #dynamic-programming #dfs #recursion
#
# A robot sits in the top-left corner of an r x c grid and wants to reach the
# bottom-right corner. It can move only RIGHT or DOWN. Some cells are "off
# limits" (marked 1) and cannot be stepped on; free cells are marked 0. Find a
# path from the top-left to the bottom-right cell, or report that none exists.
#
# Input: matrix, a list of rows of 0/1 ints. 0 = free, 1 = blocked.
# Output: a list of (row, col) coordinates from (0, 0) to (r-1, c-1) forming a
# valid right/down path over free cells, or [] if no such path exists (this also
# covers an empty grid or a blocked start/goal cell).
#
# Examples:
#   [[0, 0],
#    [1, 0]] -> [(0, 0), (0, 1), (1, 1)]
#
#   [[0, 1],
#    [1, 0]] -> []  (no unblocked right/down path)
#
#   [[0]] -> [(0, 0)]
#   [[1]] -> []  (start blocked)
#
# Approach: DFS from (0, 0) trying right then down, memoizing failed cells so
# each cell is explored at most once (O(r*c)). Build the path on the way back up.

import unittest


def find_path(matrix):
  '''
  Time: O(n x m)
  '''
  n = len(matrix)
  if n == 0:
    return []

  m = len(matrix[0])
  if m == 0:
    return []

  visited = {}

  def dfs(i, j):
    if (i, j) in visited or i == n or j == m or matrix[i][j]:
      return []

    if i == n - 1 and j == m - 1 and matrix[i][j] == 0:
      return [(i, j)]

    path = dfs(i, j + 1) or dfs(i + 1, j)
    if path:
      path.append((i, j))

    visited[(i, j)] = 1
    return path

  return list(reversed(dfs(0, 0)))


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
