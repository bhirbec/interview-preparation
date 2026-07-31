# Spiral Matrix
#
# Difficulty: medium
# Source: https://www.facebook.com/careers/life/sample_interview_questions
# Tags: #matrix #array #facebook
#
# You are given an integer n. Return an n x n matrix filled with the integers
# 1, 2, ..., n*n laid out in clockwise spiral order, starting in the top-left
# corner and moving right first.
#
# Constraints:
#   - 1 <= n <= 100
#
# Examples:
#   n = 1 -> [[1]]
#
#   n = 2 -> [[1, 2],
#             [4, 3]]
#
#   n = 3 -> [[1, 2, 3],
#             [8, 9, 4],
#             [7, 6, 5]]
#
#   n = 4 -> [[ 1,  2,  3, 4],
#             [12, 13, 14, 5],
#             [11, 16, 15, 6],
#             [10,  9,  8, 7]]
#
# Approach: keep top/bottom/left/right boundaries and walk right, down, left, up,
# shrinking a boundary after each side until they cross.


def spiral_matrix(n):
  # TODO: implement
  raise NotImplementedError
