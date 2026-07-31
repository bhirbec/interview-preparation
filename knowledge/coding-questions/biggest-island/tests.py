import unittest


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
