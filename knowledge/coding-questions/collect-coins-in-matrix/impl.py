# Collect Coins In Matrix
#
# There are N coins placed on a grid, each at an integer coordinate (x, y) with
# x >= 1 and y >= 1. You start at (0, 0). From your current position (a, b) you
# may jump to any position (a + dx, b + dy) with dx >= 1 and dy >= 1 (both
# coordinates must strictly increase on every move). You may make as many jumps
# as you like; whenever you land exactly on a coin, you collect it.
#
# You are given the list of coin coordinates. Return the maximum number of coins
# you can collect.
#
# Because every jump strictly increases both coordinates, the coins you collect
# form a sequence in which both x and y are strictly increasing. Every coin is
# reachable as a first pick (x >= 1 and y >= 1), so the answer is the length of
# the longest such chain — a two-dimensional longest-increasing-subsequence.
#
# Constraints:
#   - 0 <= N <= 1000
#   - 1 <= x, y <= 10^9
#   - two coins may share an x or a y coordinate (but not both)
#
# Examples:
#   [(1, 1), (2, 2), (3, 3)]           -> 3   (collect all three in order)
#   [(1, 3), (2, 2), (3, 1)]           -> 1   (any two conflict on x or y)
#   [(1, 1), (1, 2), (2, 3)]           -> 2   (the two x=1 coins conflict)
#   []                                 -> 0


def max_coins_collected(coins):
  # TODO: implement
  raise NotImplementedError
