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


def find_path(matrix):
  # TODO: implement
  raise NotImplementedError
