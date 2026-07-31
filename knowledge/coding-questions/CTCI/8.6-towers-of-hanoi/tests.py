import unittest


class TestTowersOfHanoi(unittest.TestCase):
  def test_zero_disks(self):
    self.assertEqual(solve_hanoi(0), [])

  def test_one_disk(self):
    self.assertEqual(solve_hanoi(1), [('A', 'C')])

  def test_two_disks(self):
    self.assertEqual(solve_hanoi(2), [('A', 'B'), ('A', 'C'), ('B', 'C')])

  def test_three_disks(self):
    self.assertEqual(
      solve_hanoi(3),
      [
        ('A', 'C'), ('A', 'B'), ('C', 'B'),
        ('A', 'C'),
        ('B', 'A'), ('B', 'C'), ('A', 'C'),
      ],
    )

  def test_move_count_is_two_pow_n_minus_one(self):
    for n in range(0, 11):
      self.assertEqual(len(solve_hanoi(n)), (1 << n) - 1)

  def test_moves_are_legal_and_finish_on_c(self):
    # Replay the moves on a fresh simulation and verify legality + end state.
    for n in range(1, 9):
      towers = {'A': list(range(n, 0, -1)), 'B': [], 'C': []}
      for origin, dest in solve_hanoi(n):
        disk = towers[origin].pop()
        self.assertTrue(not towers[dest] or towers[dest][-1] > disk)
        towers[dest].append(disk)
      self.assertEqual(towers['A'], [])
      self.assertEqual(towers['B'], [])
      self.assertEqual(towers['C'], list(range(n, 0, -1)))


if __name__ == '__main__':
  unittest.main()
