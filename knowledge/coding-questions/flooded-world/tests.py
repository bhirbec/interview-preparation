import unittest


class TestFirstDayReachable(unittest.TestCase):
  def test_two_by_two(self):
    self.assertEqual(first_day_reachable([[0, 2], [1, 3]]), 3)

  def test_leetcode_swim_example(self):
    grid = [
      [0, 1, 2, 3, 4],
      [24, 23, 22, 21, 5],
      [12, 13, 14, 15, 16],
      [11, 17, 18, 19, 20],
      [10, 9, 8, 7, 6],
    ]
    self.assertEqual(first_day_reachable(grid), 16)

  def test_single_cell(self):
    self.assertEqual(first_day_reachable([[5]]), 5)

  def test_original_example(self):
    grid = [
      [0, 9, 9, 9, 9],
      [1, 9, 9, 9, 9],
      [1, 9, 3, 2, 3],
      [2, 3, 3, 9, 2],
      [9, 9, 9, 9, 1],
    ]
    self.assertEqual(first_day_reachable(grid), 3)

  def test_straight_line_max_is_answer(self):
    # Only one path around: the answer is the highest cell that must be crossed.
    self.assertEqual(first_day_reachable([[0, 1], [8, 2]]), 2)

  def test_wall_forces_detour(self):
    # The 100 wall blocks the top; the cheapest path skirts the bottom row,
    # whose highest cell is 3.
    grid = [
      [0, 100, 5],
      [1, 100, 4],
      [2, 3, 3],
    ]
    self.assertEqual(first_day_reachable(grid), 3)

  def test_empty_grid(self):
    self.assertEqual(first_day_reachable([]), -1)


if __name__ == '__main__':
  unittest.main()
