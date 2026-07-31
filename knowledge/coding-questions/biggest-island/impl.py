# Biggest Island
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


def biggest_island(grid):
  # TODO: implement
  raise NotImplementedError
