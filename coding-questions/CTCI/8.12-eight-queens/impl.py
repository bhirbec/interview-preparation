# Eight Queens
# Difficulty: hard
# Tags: #backtracking #recursion
#
# You are given an N x N chess board. Place N queens on the board so that none
# of them can attack another, i.e. no two queens share the same row, column, or
# diagonal. Return all distinct arrangements.
#
# Input:
#   n -- the board size (number of queens), n >= 0.
# Output:
#   A list of solutions. Each solution is a list of length n where the value at
#   index r is the column of the queen placed on row r. For example [1, 3, 0, 2]
#   means row 0 has its queen in column 1, row 1 in column 3, and so on.
#
# Constraints:
#   - Exactly one queen per row (guaranteed by the placement strategy).
#   - n == 0 yields a single, empty solution (vacuously valid).
#
# Examples:
#   count of solutions for n = 0 -> 1
#   count of solutions for n = 1 -> 1
#   count of solutions for n = 4 -> 2
#   count of solutions for n = 8 -> 92
#
# Approach: classic backtracking. Place one queen per row, and for each candidate
# column check it does not collide with any already-placed queen (same column or
# same diagonal). Recurse row by row, yielding a copy of the board once all rows
# are filled.


def place_queens(n):
  # TODO: implement
  raise NotImplementedError
