# Biggest Island
#
# Difficulty: medium
# Tags: #matrix #graph #dfs
#
# You are given a rectangular grid `grid` where each cell is either "L" (land) or
# "W" (water). An island is a maximal group of land cells connected
# horizontally or vertically (NOT diagonally). Return the size (number of land
# cells) of the largest island. If the grid has no land, return 0.
#
# Constraints:
#   - 0 <= number of rows, and every row has the same number of columns
#   - each cell is either "L" or "W"
#
# Examples:
#   [["L", "W", "W", "L"],      biggest island has size 4
#    ["L", "W", "L", "L"],      (the L-shaped group on the right:
#    ["L", "W", "W", "L"]]       (0,3),(1,3),(1,2),(2,3); the left column is 3)
#
#   [["W", "L", "W", "L"],      biggest island has size 4
#    ["W", "L", "L", "W"],      (the middle group; the lone L at (0,3)/(2,3)
#    ["W", "L", "W", "L"]]       are not connected to it)
#
#   [["L"]]                     -> 1
#   [["W", "W"], ["W", "W"]]    -> 0    (no land)
#   [["L", "W"], ["W", "L"]]    -> 1    (diagonals do not connect)
#
# Approach: scan every cell; when an unvisited land cell is found, flood-fill its
# whole island with iterative DFS (4-directional), counting cells, and track the
# maximum island size seen.

import unittest


def biggest_island(grid):
  if not grid:
    return 0

  n = len(grid)
  m = len(grid[0])

  visited = {}
  max_size = 0

  for i in range(n):
    for j in range(m):
      value = grid[i][j]
      if value != 'L' or (i, j) in visited:
        continue

      size = 0
      stack = []
      stack.append((i, j))

      while len(stack) > 0:
        i, j = stack.pop()
        if (i, j) in visited:
          continue

        visited[(i, j)] = True
        size += 1

        top = (i + 1, j)
        right = (i, j + 1)
        bottom = (i - 1, j)
        left = (i, j - 1)

        for next_i, next_j in [top, right, bottom, left]:
          if 0 <= next_i < n and 0 <= next_j < m:
            adjacent_value = grid[next_i][next_j]

            if adjacent_value == 'L' or (i, j) not in visited:
              stack.append((next_i, next_j))

      if size > max_size:
        max_size = size

  return max_size


class TestBiggestIsland(unittest.TestCase):
  def test_go_source_example(self):
    grid = [
        ['L', 'W', 'W', 'L'],
        ['L', 'W', 'L', 'L'],
        ['L', 'W', 'W', 'L'],
    ]
    self.assertEqual(biggest_island(grid), 4)

  def test_comment_example(self):
    grid = [
        ['W', 'L', 'W', 'L'],
        ['W', 'L', 'L', 'W'],
        ['W', 'L', 'W', 'L'],
    ]
    self.assertEqual(biggest_island(grid), 4)

  def test_single_land_cell(self):
    self.assertEqual(biggest_island([['L']]), 1)

  def test_single_water_cell(self):
    self.assertEqual(biggest_island([['W']]), 0)

  def test_all_water(self):
    self.assertEqual(biggest_island([['W', 'W'], ['W', 'W']]), 0)

  def test_all_land(self):
    self.assertEqual(biggest_island([['L', 'L'], ['L', 'L']]), 4)

  def test_diagonal_not_connected(self):
    self.assertEqual(biggest_island([['L', 'W'], ['W', 'L']]), 1)

  def test_two_islands_returns_larger(self):
    grid = [
        ['L', 'L', 'W', 'L'],
        ['L', 'W', 'W', 'W'],
        ['W', 'W', 'L', 'L'],
    ]
    # left island: (0,0),(0,1),(1,0) = 3; right islands: {(0,3)}=1, {(2,2),(2,3)}=2
    self.assertEqual(biggest_island(grid), 3)

  def test_island_touching_all_borders(self):
    grid = [
        ['L', 'W', 'L'],
        ['L', 'L', 'L'],
        ['L', 'W', 'L'],
    ]
    # the H-shape: left column (3) + middle row bridge (2) + right column (3) = 7
    self.assertEqual(biggest_island(grid), 7)

  def test_single_row(self):
    self.assertEqual(biggest_island([['L', 'L', 'W', 'L', 'L', 'L']]), 3)

  def test_single_column(self):
    self.assertEqual(biggest_island([['L'], ['W'], ['L'], ['L']]), 2)

  def test_empty_grid(self):
    self.assertEqual(biggest_island([]), 0)


if __name__ == '__main__':
  unittest.main()
