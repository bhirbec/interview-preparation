# Rotate Matrix
#
# Difficulty: medium
# Tags: #matrix #array
#
# You are given an N x N matrix of integers. Rotate it 90 degrees
# counterclockwise IN PLACE, moving values layer by layer with four-way swaps
# and without allocating a second matrix. Return the same matrix object.
#
# Constraints:
#   - the matrix is square (N x N), N >= 0
#
# Examples:
#   [[1, 2],        rotates to   [[2, 4],
#    [3, 4]]                      [1, 3]]
#
#   [[1, 2, 3],     rotates to   [[3, 6, 9],
#    [4, 5, 6],                   [2, 5, 8],
#    [7, 8, 9]]                   [1, 4, 7]]
#
#   [[1]]           -> [[1]]
#   []              -> []
#
# Approach: process concentric layers from the outside in. For each layer, walk
# its elements and rotate them with a four-way swap (top <- right <- bottom <-
# left <- saved top), so no extra matrix is needed.


def rotate(mat):
  # TODO: implement
  raise NotImplementedError
