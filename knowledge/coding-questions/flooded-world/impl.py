# Flooded World
#
# You are given an n x n grid `grid` where grid[i][j] is the elevation of cell
# (i, j). Water rises one unit per day: on day d, every cell with elevation <= d
# is submerged and can be entered. Starting from the top-left cell (0, 0), you may
# move up, down, left, or right between submerged cells. Return the first day on
# which the bottom-right cell (n-1, n-1) becomes reachable from the start.
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
