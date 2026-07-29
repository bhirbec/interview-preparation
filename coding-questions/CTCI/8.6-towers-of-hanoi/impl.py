# Towers of Hanoi
# Difficulty: medium
# Tags: #recursion
#
# In the classic Towers of Hanoi problem you have three towers (pegs) and n
# disks of different sizes which can slide onto any tower. The puzzle starts
# with the disks stacked in ascending order of size on the first tower (the
# smallest disk on top). You must move all the disks to the last tower under
# these constraints:
#   1) only one disk may be moved at a time;
#   2) each move takes the top disk off one tower and places it on another;
#   3) a disk may never be placed on top of a smaller disk.
#
# Input:  the number of disks n >= 0. Towers are named 'A' (origin), 'B'
#         (buffer), and 'C' (destination).
# Output: the ordered list of moves that transfers all disks from A to C, each
#         move being a (source, destination) pair of tower names.
#
# Approach: to move n disks from origin to destination, recursively move the top
# n-1 disks to the buffer, move the largest disk to the destination, then move
# the n-1 disks from the buffer onto the destination. This yields exactly
# 2^n - 1 moves.
#
# Examples:
#   solve_hanoi(0) -> []
#   solve_hanoi(1) -> [('A', 'C')]
#   solve_hanoi(2) -> [('A', 'B'), ('A', 'C'), ('B', 'C')]
#   solve_hanoi(3) -> 7 moves

import unittest


def solve_hanoi(n):
  towers = {
    'A': list(range(n, 0, -1)),
    'B': [],
    'C': [],
  }
  moves = []

  def move_top(origin, dest):
    disk = towers[origin].pop()
    # A disk may never sit on a smaller one.
    assert not towers[dest] or towers[dest][-1] > disk
    towers[dest].append(disk)
    moves.append((origin, dest))

  def move_disks(k, origin, buff, dest):
    if k == 1:
      move_top(origin, dest)
      return

    move_disks(k - 1, origin, dest, buff)
    move_top(origin, dest)
    move_disks(k - 1, buff, origin, dest)

  if n > 0:
    move_disks(n, 'A', 'B', 'C')

  return moves


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
