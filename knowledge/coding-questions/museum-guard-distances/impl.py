# Museum Guard Distances
#
# A museum is represented by a square matrix whose cells are one of:
#   'O' - open space
#   'G' - a guard
#   'W' - a wall
#
# You are given the matrix. Return a new square matrix in which every 'O' is
# replaced by the number of steps to the nearest guard, moving one cell at a
# time in any of the 8 directions (horizontal, vertical, or diagonal) and never
# passing through a wall. Guard cells stay 'G' and wall cells stay 'W'. An open
# cell that cannot reach any guard stays 'O'.
#
# Constraints:
#   - 1 <= n <= 100 (matrix is n x n)
#   - cells are only 'O', 'G', or 'W'
#   - there may be zero, one, or many guards
#
# Examples:
#   [['G', 'O'],          ->   [['G', 1],
#    ['O', 'O']]                [ 1,  1]]     (diagonal reaches (1,1) in one step)
#
#   [['G', 'W', 'O']]     ->   [['G', 'W', 'O']]   (last cell is walled off)
#
#   [['G', 'O', 'O', 'G']] ->  [['G', 1, 1, 'G']]  (nearest of two guards wins)
#
#   [['O', 'O']]          ->   [['O', 'O']]        (no guard anywhere)


def museum_distances(matrix):
  # TODO: implement
  raise NotImplementedError
