# Flooded World
#
# The world is flooding. You are given an n x n grid `grid` where grid[i][j] is
# the elevation of cell (i, j). The water level rises one unit per day, so on
# day d every cell with elevation <= d is under water. You are in a boat at the
# top-left cell (0, 0), and a boat can only travel over flooded cells: on day d
# you may move up, down, left, or right between cells whose elevation is <= d.
# Return the first day on which you can reach the bottom-right cell (n-1, n-1).
# (Note the boat needs water below it even on the start and end cells.)
#
# Equivalently, among all paths from the top-left to the bottom-right, return the
# minimum possible value of the maximum elevation on the path.
#
# Constraints:
#   - 1 <= n
#   - grid is rectangular; elevations are non-negative integers
#
# Examples:
#   [[0, 2],
#    [1, 3]]                     -> 3   (path 0 -> 1 -> 3; max is 3)
#   [[0, 1, 2, 3, 4],
#    [24, 23, 22, 21, 5],
#    [12, 13, 14, 15, 16],
#    [11, 17, 18, 19, 20],
#    [10, 9, 8, 7, 6]]          -> 16  (classic "swim in rising water")
#   [[5]]                        -> 5   (single cell)


def first_day_reachable(grid):
  # TODO: implement
  raise NotImplementedError
