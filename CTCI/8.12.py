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

import unittest


def place_queens(n):
  queens = [0] * n
  return _place(n, 0, queens)


def _place(n, r, queens):
  if r > n - 1:
    yield list(queens)
    return

  for c in range(n):
    if is_valid(r, c, queens):
      queens[r] = c
      yield from _place(n, r + 1, queens)


def is_valid(r, c, queens):
  for row in range(r):
    col_delta = abs(c - queens[row])
    if col_delta == 0:
      return False

    row_delta = r - row
    if col_delta == row_delta:
      return False

  return True


def count_queens(n):
  return sum(1 for _ in place_queens(n))


class TestEightQueens(unittest.TestCase):
  def test_known_solution_counts(self):
    # Sequence A000170: number of solutions to the n-queens problem.
    expected = {0: 1, 1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92}
    for n, count in expected.items():
      self.assertEqual(count_queens(n), count, msg=f'n={n}')

  def test_n_zero_yields_single_empty_board(self):
    solutions = list(place_queens(0))
    self.assertEqual(solutions, [[]])

  def test_n_one_single_placement(self):
    self.assertEqual(list(place_queens(1)), [[0]])

  def test_n_two_and_three_have_no_solution(self):
    self.assertEqual(list(place_queens(2)), [])
    self.assertEqual(list(place_queens(3)), [])

  def test_solutions_are_valid_boards(self):
    for solution in place_queens(8):
      self.assertEqual(len(solution), 8)
      # every column used exactly once (no column collisions)
      self.assertEqual(sorted(solution), list(range(8)))
      # no two queens on the same diagonal
      for r1 in range(8):
        for r2 in range(r1 + 1, 8):
          self.assertNotEqual(abs(solution[r1] - solution[r2]), r2 - r1)

  def test_n_four_exact_solutions(self):
    solutions = sorted(place_queens(4))
    self.assertEqual(solutions, [[1, 3, 0, 2], [2, 0, 3, 1]])


if __name__ == '__main__':
  unittest.main()
