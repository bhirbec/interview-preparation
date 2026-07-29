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

import unittest


def rotate(mat):
  n = len(mat)

  for layer in range(n // 2):
    last = n - 1 - layer
    for i in range(n - 1 - 2 * layer):
      top = mat[layer][last - i]
      # right -> top
      mat[layer][last - i] = mat[last - i][last]
      # bottom -> right
      mat[last - i][last] = mat[last][layer + i]
      # left -> bottom
      mat[last][layer + i] = mat[layer + i][layer]
      # top -> left
      mat[layer + i][layer] = top

  return mat


class TestRotate(unittest.TestCase):
  def test_two_by_two(self):
    self.assertEqual(rotate([[1, 2], [3, 4]]), [[2, 4], [1, 3]])

  def test_three_by_three(self):
    mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    self.assertEqual(rotate(mat), [[3, 6, 9], [2, 5, 8], [1, 4, 7]])

  def test_single_element(self):
    self.assertEqual(rotate([[1]]), [[1]])

  def test_empty(self):
    self.assertEqual(rotate([]), [])

  def test_rotates_in_place(self):
    mat = [[1, 2], [3, 4]]
    result = rotate(mat)
    self.assertIs(result, mat)  # same object, mutated in place

  def test_four_by_four(self):
    mat = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]
    expected = [
        [4, 8, 12, 16],
        [3, 7, 11, 15],
        [2, 6, 10, 14],
        [1, 5, 9, 13],
    ]
    self.assertEqual(rotate(mat), expected)


if __name__ == '__main__':
  unittest.main()
