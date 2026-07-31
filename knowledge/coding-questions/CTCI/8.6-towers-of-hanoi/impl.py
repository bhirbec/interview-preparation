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


def solve_hanoi(n):
  # TODO: implement
  raise NotImplementedError
