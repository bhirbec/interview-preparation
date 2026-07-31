import unittest


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
