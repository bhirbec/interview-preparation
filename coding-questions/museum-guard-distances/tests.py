import unittest


class TestMuseumDistances(unittest.TestCase):
  def test_single_guard_cell(self):
    self.assertEqual(museum_distances([['G']]), [['G']])

  def test_single_open_cell_no_guard(self):
    self.assertEqual(museum_distances([['O']]), [['O']])

  def test_diagonal_move_counts_as_one(self):
    grid = [['G', 'O'],
            ['O', 'O']]
    self.assertEqual(museum_distances(grid), [['G', 1],
                                              [1, 1]])

  def test_wall_blocks_reachability(self):
    self.assertEqual(museum_distances([['G', 'W', 'O']]),
                     [['G', 'W', 'O']])

  def test_nearest_of_two_guards(self):
    self.assertEqual(museum_distances([['G', 'O', 'O', 'G']]),
                     [['G', 1, 1, 'G']])

  def test_no_guard_leaves_open_cells(self):
    self.assertEqual(museum_distances([['O', 'O'],
                                       ['O', 'O']]),
                     [['O', 'O'],
                      ['O', 'O']])

  def test_walls_and_guards_preserved(self):
    grid = [['G', 'O', 'W'],
            ['O', 'O', 'O'],
            ['W', 'O', 'G']]
    out = museum_distances(grid)
    # guards and walls untouched
    self.assertEqual(out[0][0], 'G')
    self.assertEqual(out[2][2], 'G')
    self.assertEqual(out[0][2], 'W')
    self.assertEqual(out[2][0], 'W')
    # centre is one diagonal step from either guard
    self.assertEqual(out[1][1], 1)

  def test_distance_grows_with_distance(self):
    grid = [['G', 'O', 'O', 'O']]
    self.assertEqual(museum_distances(grid), [['G', 1, 2, 3]])


if __name__ == '__main__':
  unittest.main()
