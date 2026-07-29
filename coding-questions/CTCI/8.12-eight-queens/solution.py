# A board is represented as a list `queens` where queens[r] is the column of the
# queen placed in row r. Because exactly one queen goes in each row, we only
# ever need to choose a column per row — that automatically rules out two queens
# sharing a row.


def place_queens(n):
  """Generator version: yields each valid board one at a time."""
  queens = [0] * n
  return _place(n, 0, queens)


def _place(n, r, queens):
  # Base case: every row 0..n-1 has a queen, so this is a complete solution.
  # queens is mutated in place while backtracking, so yield a *copy*.
  if r > n - 1:
    yield list(queens)
    return

  # Try placing this row's queen in each column, and recurse only into the
  # columns that don't clash with the queens already placed above.
  for c in range(n):
    if is_valid(r, c, queens):
      queens[r] = c
      yield from _place(n, r + 1, queens)


def place_queens_list(n):
  """Alternate solution without generators / `yield from`.

  Same backtracking search, but it accumulates every complete board into a
  `solutions` list and returns that list at the end. Behaves identically to
  `place_queens` (an iterable of boards), just eager instead of lazy.
  """
  solutions = []
  queens = [0] * n

  def backtrack(r):
    # A queen has been placed in every row -> record a snapshot of the board.
    # (queens keeps changing as we backtrack, so we must copy it.)
    if r == n:
      solutions.append(list(queens))
      return

    # For the current row r, try each column and recurse into the legal ones.
    for c in range(n):
      if is_valid(r, c, queens):
        queens[r] = c
        backtrack(r + 1)
      # No explicit "undo" is needed: queens[r] is simply overwritten by the
      # next column we try, and rows below r are only read once they're set.

  backtrack(0)
  return solutions


def is_valid(r, c, queens):
  """Can a queen sit at (row r, column c) given the queens already in rows < r?"""
  for row in range(r):
    col_delta = abs(c - queens[row])

    # Same column -> they attack vertically.
    if col_delta == 0:
      return False

    # Equal horizontal and vertical distance -> they share a diagonal.
    row_delta = r - row
    if col_delta == row_delta:
      return False

  return True
