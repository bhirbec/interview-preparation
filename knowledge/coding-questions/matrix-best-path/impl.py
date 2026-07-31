# Matrix Best Path
#
# You are given an R x C matrix that contains each integer from 1 to R*C exactly
# once (all values are distinct). A path goes from the top-left corner to the
# bottom-right corner, where every step moves either one cell down or one cell to
# the right.
#
# To compare two paths, take the multiset of values along each path and sort it
# ascending; the "better" path is the one whose sorted list is lexicographically
# smaller (e.g. [1, 3, 4, 5, 7] < [1, 4, 5, 6, 7]).
#
# Return the values of the best path in path order (top-left to bottom-right).
#
# Constraints:
#   - 1 <= R, C
#   - the matrix is a permutation of 1..R*C
#
# Examples:
#   [[4, 5, 9],
#    [8, 1, 3],     -> [4, 5, 1, 3, 7]
#    [2, 6, 7]]
#
#   [[1]]           -> [1]
#   [[1, 2, 3]]     -> [1, 2, 3]   (single row)
#   [[1], [2], [3]] -> [1, 2, 3]   (single column)


def find_best_path(matrix):
  # TODO: implement
  raise NotImplementedError
