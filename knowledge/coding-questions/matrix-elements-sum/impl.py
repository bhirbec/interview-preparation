# Matrix Elements Sum
#
# You are given a matrix of integers `matrix` where matrix[i][j] is the price of
# the room on floor i, column j of a hotel (row 0 is the top floor). A price of 0
# means that room is unavailable, and — because guests are superstitious — every
# room directly below an unavailable room, in the same column, is also considered
# unavailable, regardless of its own price.
#
# Return the total price of all available rooms: for each column, add up prices
# from the top floor downward, stopping as soon as you reach a 0 in that column.
#
# Constraints:
#   - 1 <= len(matrix), len(matrix[0]) <= 100
#   - 0 <= matrix[i][j] <= 10000
#   - every row has the same number of columns
#
# Examples:
#   [[0, 1, 1, 2],       col sums: 0 | 1+5 | 1 | 2   -> 9
#    [0, 5, 0, 0],
#    [2, 0, 3, 3]]
#
#   [[1, 1, 1, 0],       col sums: 1 | 1+5+1 | 1 | 0 -> 9
#    [0, 5, 0, 1],
#    [2, 1, 3, 10]]
#
#   [[0]]                col sums: 0                  -> 0
#   [[1, 5], [3, 2]]     col sums: 1+3 | 5+2          -> 11


def matrix_elements_sum(matrix):
  # TODO: implement
  raise NotImplementedError
