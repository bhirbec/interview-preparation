import unittest


class TestFindBase(unittest.TestCase):
  def test_single_site(self):
    self.assertEqual(find_base(["*", " "]), (0, 0))

  def test_no_sites(self):
    self.assertIsNone(find_base(["   ", "   "]))

  def test_empty_grid(self):
    self.assertIsNone(find_base([]))

  def test_unreachable_sites(self):
    self.assertIsNone(find_base(["*#", "#*"]))

  def test_geometric_median(self):
    self.assertEqual(find_base(["*   ", "    ", "*  *"]), (2, 0))

  def test_row_major_tie_break(self):
    # Two sites stacked in column 0; cells (0,0) and (1,0) both total 1.
    self.assertEqual(find_base(["*  ", "*  ", "   "]), (0, 0))

  def test_wall_lengthens_path(self):
    # The '#' wall forces the base toward the corridor around it.
    grid = [
      "*  ",
      "## ",
      "  *",
    ]
    self.assertTrue(all(len(row) == len(grid[0]) for row in grid))
    result = find_base(grid)
    # Both sites must be reachable, so the answer is a real cell.
    self.assertIsNotNone(result)
    r, c = result
    self.assertNotEqual(grid[r][c], '#')

  def test_base_on_a_site(self):
    # With sites adjacent, placing the base on a site minimizes the total.
    self.assertEqual(find_base(["**"]), (0, 0))


if __name__ == '__main__':
  unittest.main()
