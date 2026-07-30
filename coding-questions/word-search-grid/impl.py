# Word Search
#
# Difficulty: medium
# Tags: #matrix #dfs #backtracking #uber
#
# You are given a rectangular `grid` of letters and a `word`. Return True if the
# word can be traced through the grid, subject to these rules:
#   1. Start from any cell.
#   2. Move one step at a time, horizontally or vertically only (no diagonals).
#   3. The same cell may not be used more than once in a single path.
# Return False if no such path exists.
#
# Constraints:
#   - 1 <= number of rows, 1 <= number of columns
#   - word is non-empty
#
# Examples:
#   grid = [["A", "R", "I", "D", "S"],
#           ["W", "E", "R", "O", "D"],
#           ["U", "E", "F", "B", "E"],
#           ["B", "E", "R", "E", "E"]]
#   word = "UBER"  -> True   (U at (2,0) -> B (3,0) -> E (3,1) -> R (3,2))
#
#   grid = [["A", "B"], ["C", "D"]]
#   word = "ABDC" -> True    (A -> B -> D -> C, an L-shaped path)
#   word = "ABCD" -> False   (B and C are not adjacent)
#   word = "AA"   -> False   (cannot reuse the single A)
#
# Approach: from every cell that matches the first letter, run a depth-first
# search that marks the cell visited, recurses into the four neighbors for the
# next letter, then unmarks it on backtrack.


def word_search(grid, word):
  # TODO: implement
  raise NotImplementedError
